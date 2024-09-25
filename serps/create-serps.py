#!/usr/bin/env python3
from tira.tirex import IRDS_TO_TIREX_DATASET
import os
os.environ['IR_DATASETS_HOME'] = '/mnt/ceph/tira/state/ir_datasets/'
import ir_datasets
from glob import glob
from tqdm import tqdm
from trectools import TrecRun
from diffir import WeightBuilder
from diffir.dynamic_ir_datasets_loader import GenericDocFromDict
from pathlib import Path
import json
from diffir.run import MainTask
TIREX_DATASET_TO_IRDS = {v:k for k,v in IRDS_TO_TIREX_DATASET.items()}
DATASET_IDS = set(['msmarco-passage-trec-dl-2019-judged-20230107-training', 'msmarco-passage-trec-dl-2020-judged-20230107-training', 'disks45-nocr-trec-robust-2004-20230209-training', 'clueweb12-trec-web-2013-20230107-training', 'clueweb12-trec-web-2014-20230107-training', 'clueweb09-en-trec-web-2009-20230107-training', 'clueweb09-en-trec-web-2010-20230107-training', 'clueweb09-en-trec-web-2011-20230107-training', 'clueweb09-en-trec-web-2012-20230107-training'])
diffir = MainTask(measure='qrel', weight={"weights_1": None, "weights_2": None})

def main(dataset_id):
    irds_id = TIREX_DATASET_TO_IRDS[dataset_id]
    runs = glob(f'/mnt/ceph/tira/data/runs/{dataset_id}/**/**/**/run.txt')
    print(dataset_id, ':', irds_id, len(runs))
    dataset = ir_datasets.load(irds_id)
    docs_store = dataset.docs_store()
    qid_to_query = {str(i.query_id): i for i in dataset.queries_iter()}
    qid_to_docs = {}
    for run in tqdm(runs):
        run = TrecRun(run).run_data
        run = run[run['rank'] <= 11]
        for _, i in run.iterrows():
            if i['query'] not in qid_to_docs:
                qid_to_docs[i['query']] = set()
            qid_to_docs[i['query']].add(i['docid'])

    for qrel in dataset.qrels_iter():
        qid_to_docs[qrel.query_id].add(qrel.doc_id)

    for qid in tqdm(qid_to_docs):
        snippets = {}
        for doc_id in qid_to_docs[qid]:
            # from diffir: https://github.com/capreolus-ir/diffir/blob/master/diffir/run.py#L147C32-L147C38
            try:
                doc = docs_store.get(doc_id)
            except:
                pass

            if not doc:
                snippets[doc_id] = {'snippet': '', 'weights': {}}
                continue

            doc = GenericDocFromDict({'text': doc.default_text(), 'original_document': {'doc_id': doc.doc_id}})

            weights = diffir.weight.score_document_regions(qid_to_query[qid], doc, 0)
            snippet = diffir.find_snippet(weights, doc)
            assert snippet['field'] == 'text'
            if snippet['start'] != 0:
                snippet['weights'] = [[i[0] + 3, i[1] + 3, i[2]] for i in snippet['weights']]
            
            text = ('' if snippet['start'] == 0 else '...') + doc.text[snippet['start']: snippet['stop']] + ('' if snippet['stop'] >= (len(doc.text) - 20) else '...')

            snippets[doc_id] = {'snippet': text, 'weights': snippet['weights']}
        output_file = Path(f'/mnt/ceph/tira/data/publicly-shared-datasets/tirex-snippets/{dataset_id}')
        output_file.mkdir(exist_ok=True)
        with open(output_file / qid, 'w') as f:
            f.write(json.dumps(snippets))


if __name__ == '__main__':
    for tirex_dataset in IRDS_TO_TIREX_DATASET.values():
        if tirex_dataset not in DATASET_IDS:
            continue
        main(tirex_dataset)
