#!/usr/bin/env python3
import argparse
import os

from tira.third_party_integrations import ensure_pyterrier_is_loaded, load_rerank_data, persist_and_normalize_run


def parse_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--input', type=str, help='The directory with the input data (i.e., a queries.jsonl and a documents.jsonl file).', required=True)
    parser.add_argument('--model', default=os.environ['MODEL_NAME'])
    parser.add_argument('--output', type=str, help='The output will be stored in this directory.', required=True)
    
    return parser.parse_args()


def rerank(model, input_directory, output_directory):
    df = load_rerank_data(input_directory)
    from pyterrier_colbert.ranking import ColBERTFactory
    pytcolbert = ColBERTFactory(model, "/index", "index")
    ret = pytcolbert.text_scorer(verbose=True)(df)
    
    persist_and_normalize_run(ret, 'colbert', output_directory)


if __name__ == '__main__':
    args = parse_args()
    ensure_pyterrier_is_loaded()

    rerank(args.model, args.input, args.output)

