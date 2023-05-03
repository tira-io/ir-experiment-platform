#!/usr/bin/env python3
import os
import argparse
import pandas as pd
from beir.retrieval import models
from tqdm import tqdm
from tira.third_party_integrations import load_rerank_data, persist_and_normalize_run
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES


def parse_args():
    parser = argparse.ArgumentParser(prog='Retrieve with DenseRetrievalExactSearch models of BEIR.')

    parser.add_argument('--model', default=os.environ['DRES_MODEL'])
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--score_function', choices=['cos_sim', 'dot'], required=True)
    parser.add_argument('--batch_size', default=128)
    parser.add_argument('--corpus_chunk_size', default=50000)

    return vars(parser.parse_args())


def rank(df_queries, df_docs, sbert_model, score_function, batch_size, corpus_chunk_size):
    print(f'Rank {len(df_docs)} documents for {len(df_queries)} queries.')
    model = DRES(sbert_model, batch_size=int(batch_size), corpus_chunk_size=int(corpus_chunk_size))

    corpus = {i['docno']:{'text': i['text']} for _, i in df_docs.iterrows()}
    queries = {i['qid']: i['query'] for _, i in df_queries.iterrows()}

    scores = model.search(corpus=corpus, queries=queries, top_k=1000, score_function=score_function, return_sorted=True)
    ret = []

    for qid in scores:
        for doc_id in scores[qid]:
            ret += [{'qid': qid, 'Q0': 0, 'docno': doc_id, 'score': scores[qid][doc_id]}]

    return ret


def main(model, input, output, score_function, batch_size, corpus_chunk_size):
    df_docs = pd.read_json(f'{input}/documents.jsonl', lines=True)
    df_queries = pd.read_json(f'{input}/queries.jsonl', lines=True)
    sbert_model = models.SentenceBERT(model)

    ret = rank(df_queries, df_docs, sbert_model, score_function, batch_size, corpus_chunk_size)

    persist_and_normalize_run(pd.DataFrame(ret), model + '-' + score_function, output)


if __name__ == '__main__':
    args = parse_args()
    main(**args)

