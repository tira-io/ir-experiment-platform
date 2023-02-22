#!/usr/bin/env python3
import os
import argparse
import pandas as pd
from tqdm import tqdm
from tira.third_party_integrations import load_rerank_data, persist_and_normalize_run
from pygaggle.rerank.base import Query, Text
import importlib
from pygaggle.rerank.transformer import MonoT5, MonoBERT


def parse_args():
    parser = argparse.ArgumentParser(prog='Re-rank with pygaggle.')

    parser.add_argument('--model_name', default=os.environ['MODEL_NAME'])
    parser.add_argument('--tokenizer_name', default=os.environ['TOKENIZER_NAME'])
    parser.add_argument('--input', help='The directory with the input data (i.e., a queries.jsonl and a documents.jsonl file).', required=True)
    parser.add_argument('--output', type=str, help='The output will be stored in this directory.', required=True)

    return parser.parse_args()


def rerank(qid, query, df_docs, model):
    print(f'Rerank for query "{query}" (qid={qid}).')

    texts = [Text(i['text'], {'docid': i['docno']}, 0) for _, i in df_docs.iterrows()]
    
    scores = model.rerank(Query(query), texts)
    scores = {i.metadata["docid"]: i.score for i in scores}
    ret = []

    for _, i in df_docs.iterrows():
        ret += [{'qid': qid, 'Q0': 0, 'docno': i['docno'], 'score': scores[i['docno']], 'rank': 0}]

    return ret


def main(model_name, tokenizer_name, input_file, output_directory):
    df = load_rerank_data(input_file)
    qids = sorted(list(df['qid'].unique()))
    df_ret = []
    model = None
    
    if 'monot5' in model_name.lower():
        model = MonoT5(model=MonoT5.get_model(model_name, local_files_only=True), tokenizer=MonoT5.get_tokenizer(tokenizer_name, local_files_only=True))
    elif 'monobert' in model_name.lower():
        model = MonoBERT(model=MonoBERT.get_model(model_name, local_files_only=True), tokenizer=MonoBERT.get_tokenizer(tokenizer_name, local_files_only=True))

    for qid in tqdm(qids):
        df_qid = df[df['qid'] == qid]
        query = df_qid.iloc[0].to_dict()['query']

        df_ret += rerank(qid, query, df_qid[['docno', 'text']], model)

    persist_and_normalize_run(pd.DataFrame(df_ret), model_name, output_directory)


if __name__ == '__main__':
    args = parse_args()
    main(args.model_name, args.tokenizer_name, args.input, args.output)

