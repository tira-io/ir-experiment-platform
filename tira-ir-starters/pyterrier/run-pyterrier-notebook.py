#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess


def parse_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--input', type=str, help='The directory that contains the input data (this directory is expected to contain a queries.jsonl and a documents.jsonl file).', required=True)
    parser.add_argument('--notebook', type=str, help='The notebook to execute.', required=True)
    parser.add_argument('--output', type=str, help='The resulting run.txt will be stored in this directory.', required=True)

    return parser.parse_args()


def main(args):
    os.environ['TIRA_INPUT_DIRECTORY'] = args.input
    os.environ['TIRA_OUTPUT_DIRECTORY'] = args.output

    command = f'runnb --allow-not-trusted {args.notebook}'
    subprocess.check_call(command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)


if __name__ == '__main__':
    main(parse_args())

