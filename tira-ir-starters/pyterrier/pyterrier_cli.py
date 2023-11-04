#!/usr/bin/env python3

import json
import argparse
from pathlib import Path
import os

from tira.third_party_integrations import ensure_pyterrier_is_loaded, load_rerank_data, normalize_run
import pyterrier as pt
from pyterrier import IndexRef
import gzip
import importlib
from tqdm import tqdm


def process_params_input(params: list):
    return { param.partition('=')[0]: param.partition('=')[2] for param in params } if params else {}


def load_retrieval_pipeline(pipeline: str, indexref: IndexRef, controls: dict):
    pipeline = pipeline.split('.')
    
    module_name = '.'.join(pipeline[:-1])
    module = importlib.import_module(module_name)
    
    return getattr(module, pipeline[-1])(indexref, controls)


def parse_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--input', type=str, help='The directory with the input data (i.e., a queries.jsonl and a documents.jsonl file).', required=True)
    parser.add_argument('--output', type=str, help='The output will be stored in this directory.', required=True)
    parser.add_argument('--index_directory', type=str, help='The index is stored/expected in this directory.', required=False)
    parser.add_argument('--retrieval_pipeline', type=str, default=None, help='TBD.')
    parser.add_argument('--params', type=str, nargs='+', help='The controls of the retrieval methods as dictionaries.', required=False)
    parser.add_argument('--rerank', type=bool, default=False, help='Run a re-ranker. This assumes that the input directory contains a valid re-ranking input.', required=False)
    parser.add_argument('--blocks', type=bool, default=False, help='For indexing: should the pyterrier index add blocks?', required=False)
    
    return parser.parse_args()


def index(documents, index_directory, blocks):
    if os.path.exists(f'{index_directory}/data.properties'):
        return pt.IndexRef.of(f'{index_directory}/data.properties')

    if Path(documents).exists():
        documents = tqdm((json.loads(line) for line in Path(documents).open('rt')), 'Load Documents')
    elif Path(documents +'.gz').exists():
        documents = tqdm((json.loads(line) for line in gzip.open(documents + '.gz', 'rt')), 'Load Documents')

    print(f'create new index at:\t{index_directory}')
    return pt.IterDictIndexer(index_directory, meta={'docno' : 100}, blocks=blocks).index(documents)


def retrieve(queries, index_ref, args, retrieval_pipeline, output_directory):
    print(f'loading topics from:\t{queries}')
    queries = pt.io.read_topics(queries, 'trecxml')
    
    controls = process_params_input(args.params)
    controls['raw_passed_arguments'] = vars(args)
    pipeline = load_retrieval_pipeline(retrieval_pipeline, index_ref, controls)
    
    result = pipeline(queries)

    print(f'writing run file to:\t{output_directory}/run.txt')
    Path(output_directory).mkdir(parents=True, exist_ok=True)
    pt.io.write_results(normalize_run(result, 1000), f'{output_directory}/run.txt', run_name=f'pyterrier.{retrieval_pipeline}')


def rerank(rerank_data, retrieval_pipeline, output_directory):
    pipeline = load_retrieval_pipeline(retrieval_pipeline, None, process_params_input(args.params))
    
    rerank_data['query'] = rerank_data['query'].apply(lambda i: "".join([x if x.isalnum() else " " for x in i]))

    result = pipeline(rerank_data)

    print(f'writing run file to:\t{output_directory}/run.txt')
    Path(output_directory).mkdir(parents=True, exist_ok=True)
    pt.io.write_results(normalize_run(result, 1000), f'{output_directory}/run.txt', run_name=f'pyterrier.{retrieval_pipeline}')

if __name__ == '__main__':
    args = parse_args()
    ensure_pyterrier_is_loaded()

    index_ref = index(args.input + '/documents.jsonl', os.path.abspath(Path(args.index_directory) / 'index'), args.blocks) if args.index_directory else None

    if args.retrieval_pipeline:
        if args.rerank:
            rerank(load_rerank_data(args.input), args.retrieval_pipeline, args.output)
        else:
            retrieve(args.input + '/queries.xml', index_ref, args, args.retrieval_pipeline, args.output)

