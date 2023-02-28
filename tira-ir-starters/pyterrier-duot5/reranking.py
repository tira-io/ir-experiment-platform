#!/usr/bin/env python3
import argparse
import os

from tira.third_party_integrations import ensure_pyterrier_is_loaded, load_rerank_data
ensure_pyterrier_is_loaded()

import math
import pandas as pd
import pyterrier as pt
import torch
from torch.nn import functional as F
from transformers import T5Config, T5Tokenizer, T5ForConditionalGeneration
from pyterrier.transformer import TransformerBase
import itertools
import json

class DuoT5PairwisePreferences(TransformerBase):
    def __init__(self, tok_model: str = 't5-base', model: str = 'castorini/duot5-base-msmarco',
                 batch_size: int = 4, text_field: str = 'text', verbose=True):
        self.verbose = verbose
        self.batch_size = batch_size
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = T5Tokenizer.from_pretrained(tok_model, model_max_length=512)
        self.model_name = model
        self.model = T5ForConditionalGeneration.from_pretrained(model)
        self.model.to(self.device)
        self.model.eval()
        self.text_field = text_field
        self.REL = self.tokenizer.encode('true')[0]
        self.NREL = self.tokenizer.encode('false')[0]

    def transform(self, run):
        queries, texts = run['query'], run[self.text_field]
        pairwise_scores = []
        all_queries = set(queries.unique())
        prompts = self.tokenizer.batch_encode_plus([f'Relevant:' for _ in range(self.batch_size)], return_tensors='pt',
                                                   padding='longest')
        max_vlen = self.model.config.n_positions - prompts['input_ids'].shape[1]
        batches = 0
        for batch in self._iter_duo_batches(run):
            batches += 1
            enc_query = self.tokenizer.batch_encode_plus([f'Query: {q}' for q in batch['query']], return_tensors='pt',
                                                         padding='longest')
            enc_text0 = self.tokenizer.batch_encode_plus([f'Query: {q}' for q in batch['text0']], return_tensors='pt',
                                                         padding='longest')
            enc_text1 = self.tokenizer.batch_encode_plus([f'Query: {q}' for q in batch['text1']], return_tensors='pt',
                                                         padding='longest')
            enc = {}
            for key in enc_query:
                query = enc_query[key][:, :-1]  # chop off end of sequence token-- this will be added with the prompt
                text0 = enc_text0[key][:, :-1]  # chop off end of sequence token-- this will be added with the prompt
                text1 = enc_text1[key][:, :-1]  # chop off end of sequence token-- this will be added with the prompt
                # Do we need to truncate? If so, how many tokens per document?
                if query.shape[1] + text0.shape[1] + text1.shape[1] > max_vlen:
                    tokens_to_truncate = query.shape[1] + text0.shape[1] + text1.shape[1] - max_vlen
                    tokens_to_truncate_per_doc = math.ceil(tokens_to_truncate / 2)
                    text0 = text0[:, :-tokens_to_truncate_per_doc]
                    text1 = text1[:, :-tokens_to_truncate_per_doc]
                # Combine the components:
                enc[key] = torch.cat([query, text0, text1, prompts[key][:query.shape[0]]], dim=1)
            enc['decoder_input_ids'] = torch.full(
                (len(batch['ids']), 1),
                self.model.config.decoder_start_token_id,
                dtype=torch.long
            )
            enc = {k: v.to(self.device) for k, v in enc.items()}
            with torch.no_grad():
                result = self.model(**enc).logits
            result = result[:, 0, (self.REL, self.NREL)]
            result = F.log_softmax(result, dim=1)[:, 0].cpu().detach().tolist()

            for (qid, did1, did2), score in zip(batch['ids'], result):
                yield {'qid': qid, 'docno1': did1, 'docno2': did2, 'score': score}

    def _iter_duo_pairs(self, run):
        warned = False
        groups = run.groupby('qid')
        if self.verbose:
            groups = pt.tqdm(groups, desc='duoT5', unit='queries')
        for qid, group in groups:
            if not warned and len(group) > 50:
                warnings.warn(f'A large number of results per query was detected ({len(group)}). Since DuoT5 '
                               'is an O(n^2) operation, this will take a considerable amount of time to process. '
                               'Consider first reducing the size of the results using the % operator.')
                warned = True
            for row1, row2 in itertools.permutations(group.itertuples(index=False), 2):
                yield row1.qid, row1.query, getattr(row1, self.text_field), getattr(row2, self.text_field), row1.docno, row2.docno

    def _iter_duo_batches(self, run):
        batch = {'ids': [], 'query': [], 'text0': [], 'text1': []}
        print('We shorten queries to the first 1000 characters and both documents each to the first 4000 characters....')
        for qid, query, text0, text1, did0, did1 in self._iter_duo_pairs(run):
            batch['ids'].append((qid, did0, did1))
            batch['query'].append(query[:1000])
            batch['text0'].append(text0[:4000])
            batch['text1'].append(text1[:4000])
            if len(batch['ids']) == self.batch_size:
                yield batch
                for v in batch.values():
                    v.clear()
        if len(batch['ids']) > 0:
            yield batch


def parse_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--input', type=str, help='The directory with the input data (i.e., a queries.jsonl and a documents.jsonl file).', required=True)
    parser.add_argument('--model', default=os.environ['MODEL_NAME'])
    parser.add_argument('--tokenizer', default=os.environ['TOKENIZER_NAME'])
    parser.add_argument('--top_k', type=int, help="how many documents to rerank", required=True)
    parser.add_argument('--output', type=str, help='The output will be stored in this directory.', required=True)
    
    return parser.parse_args()


def rerank(model, tok_model, top_k, input_directory, output_directory):

    df = load_rerank_data(input_directory)
    df = df[df['rank'] <= top_k]
    duot5 = DuoT5PairwisePreferences(model=model, tok_model=tok_model)
    
    with open(output_directory +'/pairwise-preferences.jsonl', 'w') as out_file:
        for pref in duot5(df):
            out_file.write(json.dumps(pref) + '\n')
    pairwise_aggregation(output_directory)


def pairwise_aggregation(input_directory):
    import os
    import pandas as pd
    from tira.third_party_integrations import persist_and_normalize_run
    import json
    run_output = input_directory + '/run.txt'

    if os.path.isfile(run_output):
        return
    
    scores = {}

    with open(input_directory +'/pairwise-preferences.jsonl', 'r') as preferences:
        for l in preferences:
            l = json.loads(l)
            qid, id_a, id_b, score = l['qid'], l['docno1'], l['docno2'], l['score']
            if qid not in scores:
                scores[qid] = {}

            for doc_id in [id_a, id_b]:
                if doc_id not in scores[qid]:
                    scores[qid][doc_id] = 0

            scores[qid][id_a] += score
            scores[qid][id_b] += (1 - score)

    ret = []

    for qid in scores:
        for doc_id in scores[qid].keys():
             ret += [{'qid': qid, 'Q0': 0, 'docno': doc_id, 'score': scores[qid][doc_id], 'rank': 0}]

    persist_and_normalize_run(pd.DataFrame(ret), 'duoT5-additive', input_directory)


if __name__ == '__main__':
    args = parse_args()

    rerank(args.model, args.tokenizer, args.top_k, args.input, args.output)

