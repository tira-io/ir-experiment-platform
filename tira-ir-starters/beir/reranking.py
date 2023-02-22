#!/usr/bin/env python3
import os
import argparse
import pandas as pd
from beir.retrieval import models
from tqdm import tqdm
from tira.third_party_integrations import load_rerank_data, persist_and_normalize_run
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES


def parse_args():
    parser = argparse.ArgumentParser(prog='Re-rank with DenseRetrievalExactSearch models of BEIR.')

    parser.add_argument('--model', default=os.environ['DRES_MODEL'])
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--score_function', choices=['cos_sim', 'dot'], required=True)
    parser.add_argument('--batch_size', default=128)
    parser.add_argument('--corpus_chunk_size', default=50000)

    return vars(parser.parse_args())


def rerank(qid, query, df_docs, sbert_model, score_function, batch_size, corpus_chunk_size):
    print(f'Rerank for query "{query}" (qid={qid}).')
    model = DRES(sbert_model, batch_size=int(batch_size), corpus_chunk_size=int(corpus_chunk_size))

    corpus = {i['docno']:{'text': i['text']} for _, i in df_docs.iterrows()}
    queries = {qid: query, str(qid) + '-duplicate': query}

    scores = model.search(corpus=corpus, queries=queries, top_k=2*len(corpus), score_function=score_function, return_sorted=True)[qid]
    ret = []

    for _, i in df_docs.iterrows():
        ret += [{'qid': qid, 'Q0': 0, 'docno': i['docno'], 'score': scores.get(i['docno'], 0)}]

    return ret


def main(model, input, output, score_function, batch_size, corpus_chunk_size):
    df = load_rerank_data(input)
    sbert_model = models.SentenceBERT(model)
    qids = sorted(list(df['qid'].unique()))
    df_ret = []

    for qid in tqdm(qids):
        df_qid = df[df['qid'] == qid]
        query = df_qid.iloc[0].to_dict()['query']

        df_ret += rerank(qid, query, df_qid[['docno', 'text']], sbert_model, score_function, batch_size, corpus_chunk_size)

    persist_and_normalize_run(pd.DataFrame(df_ret), model + '-' + score_function, output)


if __name__ == '__main__':
    args = parse_args()
    main(**args)

