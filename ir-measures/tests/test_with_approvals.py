import io
import os
import sys
from contextlib import redirect_stdout
from pathlib import Path
from shutil import copytree
from tempfile import TemporaryDirectory
from typing import List

from approvaltests import set_default_reporter, DiffReporter
from approvaltests.approvals import verify
from pytest import raises
import shutil

from ir_measures_evaluator import main

_TEST_IO_DIR = Path(__file__).parent / 'test-io'
_TEST_OUTPUT_DIR = '<token-to-be-replaced-by-test-output>'


def setup_module():
    set_default_reporter(DiffReporter())


def run_capture_stdout_files(
        argv: List[str],
        exit_normal: bool,
        output_dir: str = 'test-output',
):
    buffer = io.StringIO()
    captured_files = ''
    with TemporaryDirectory() as temp_dir:
        tmp_path = Path(temp_dir) / 'test-io'
        copytree(_TEST_IO_DIR, tmp_path)
        
        # Override sys.argv
        sys.argv = ['', *argv]
        sys.argv = [i.replace(_TEST_OUTPUT_DIR, str(tmp_path)) for i in sys.argv]

        with redirect_stdout(buffer):
            if exit_normal:
                main()
            else:
                with raises(SystemExit):
                    main()

        # List files in temp output dir
        files = sorted((tmp_path/output_dir).glob('**/*'))
        filenames = [
            str(file.relative_to(tmp_path)) for file in files
        ]
        captured_files += f'\n\n####\nfiles: {filenames}\n'
        for file in files:
            if not file.is_file() or '.data-top-10-for-rendering.json.gz' in str(file):
                continue
            captured_files += f'\n\n####{file.relative_to(tmp_path)}\n' + \
                              open(file).read()

    return buffer.getvalue()\
        .replace(str(_TEST_IO_DIR) + '/', '')\
        .replace(str(tmp_path/output_dir), output_dir)\
        .replace(str(tmp_path), '<output-dir>/') + '\n'.join([i for i in captured_files.split('\n') if not i.strip().startswith('var data =')])


def _run_capture_stdout_files_fail(
        argv: List[str],
        output_dir: str = 'test-output',
):
    return run_capture_stdout_files(argv, False, output_dir)


def _run_capture_stdout_files_pass(
        argv: List[str],
        output_dir: str = 'test-output',
):
    return run_capture_stdout_files(argv, True, output_dir)



def test_run_path_is_dir():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input', '--output', '.'
    ])
    verify(actual)


def test_run_file_empty():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/empty_file.txt',  '--output', '.'
    ])
    verify(actual)


def test_run_fewer_columns():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_invalid_less_columns.txt',  '--output', '/tmp'
    ])
    verify(actual)


def test_qrels_path_not_found():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', 'bar',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
    ])
    verify(actual)


def test_qrels_path_is_dir():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
    ])
    verify(actual)

def test_qrels_file_empty():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/empty_file.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
    ])
    verify(actual)


def test_qrels_valid_no_topics():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--output', '/tmp'
    ])
    verify(actual)


def test_topics_path_not_found():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--topics', 'baz',
    ])
    verify(actual)


def test_topics_path_is_dir():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input',
    ])
    verify(actual)


def test_topics_file_empty():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/empty_file.jsonl',
    ])
    verify(actual)


def test_topics_valid_no_qrels():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
        '--output', '/tmp'
    ])
    verify(actual)


#def test_query_ids_inconsistent_topics_run():
#    actual = _run_capture_stdout_files_pass([
#        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
#        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_warning_qid_not_in_run.jsonl',
#        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
#    ])
#    verify(actual)


def test_measure_unknown():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
        '--measures', 'FOOBAR',
    ])
    verify(actual)


def test_measure_invalid():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
        '--measures', 'P@X',
    ])
    verify(actual)


def test_measure_valid():
    actual = _run_capture_stdout_files_pass([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2',
    ])
    verify(actual)


def test_measures_valid():
    actual = _run_capture_stdout_files_pass([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2', 'nDCG@2',
    ])
    verify(actual)


def test_output_path_not_found():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2', 'nDCG@2',
        '--output', '42',
    ])
    verify(actual)


def test_output_path_is_file():
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2', 'nDCG@2',
        '--output', f'{_TEST_IO_DIR}/test-output-not-empty/file.txt',
    ])
    verify(actual)


def test_output_dir_not_empty():
    actual = _run_capture_stdout_files_pass([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2', 'nDCG@2',
        '--output', f'{_TEST_OUTPUT_DIR}/test-output-not-empty',
    ], output_dir='test-output-not-empty')
    verify(actual)


def test_output_valid_no_qrels():
    shutil.rmtree(_TEST_IO_DIR / 'test-output', ignore_errors=True)
    (_TEST_IO_DIR / 'test-output').mkdir(exist_ok=True, parents=True)
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2', 'nDCG@2',
        '--output', f'{_TEST_OUTPUT_DIR}/test-output',
    ])
    shutil.rmtree(_TEST_IO_DIR / 'test-output', ignore_errors=True)
    verify(actual)


def test_output_valid_no_topics():
    shutil.rmtree(_TEST_IO_DIR / 'test-output', ignore_errors=True)
    (_TEST_IO_DIR / 'test-output').mkdir(exist_ok=True, parents=True)
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--measures', 'P@2', 'nDCG@2',
        '--output', f'{_TEST_OUTPUT_DIR}/test-output',
    ])
    shutil.rmtree(_TEST_IO_DIR / 'test-output', ignore_errors=True)
    verify(actual)


def test_output_valid_no_measures():
    shutil.rmtree(_TEST_IO_DIR / 'test-output', ignore_errors=True)
    (_TEST_IO_DIR / 'test-output').mkdir(exist_ok=True, parents=True)
    actual = _run_capture_stdout_files_fail([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
        '--output', f'{_TEST_OUTPUT_DIR}/test-output',
    ])
    shutil.rmtree(_TEST_IO_DIR / 'test-output', ignore_errors=True)
    verify(actual)


def test_all_valid():
    shutil.rmtree(_TEST_IO_DIR / 'test-output', ignore_errors=True)
    (_TEST_IO_DIR / 'test-output').mkdir(exist_ok=True, parents=True)
    actual = _run_capture_stdout_files_pass([
        '--run', f'{_TEST_IO_DIR}/test-input/run_sample_valid.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/qrels_sample_valid.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2', 'nDCG@2',
        '--output', f'{_TEST_OUTPUT_DIR}/test-output',
    ])
    shutil.rmtree(_TEST_IO_DIR / 'test-output', ignore_errors=True)
    verify(actual)

def test_all_valid_with_rendering():
    shutil.rmtree(_TEST_IO_DIR / 'test-output', ignore_errors=True)
    (_TEST_IO_DIR / 'test-output').mkdir(exist_ok=True, parents=True)
    actual = _run_capture_stdout_files_pass([
        '--run', f'{_TEST_IO_DIR}/test-input/test-input-cranfield/run.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/test-input-cranfield/qrels.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/test-input-cranfield/queries.jsonl',
        '--measures', 'P@2', 'nDCG@2',
        '--output', f'{_TEST_OUTPUT_DIR}/test-output',
    ])
    shutil.rmtree(_TEST_IO_DIR / 'test-output', ignore_errors=True)
    verify(actual)

def test_all_valid_with_rendering_wrong_qrels_and_queries():
    shutil.rmtree(_TEST_IO_DIR / 'test-output', ignore_errors=True)
    (_TEST_IO_DIR / 'test-output').mkdir(exist_ok=True, parents=True)
    actual = _run_capture_stdout_files_pass([
        '--run', f'{_TEST_IO_DIR}/test-input/test-input-cranfield/run.txt',
        '--qrels', f'{_TEST_IO_DIR}/test-input/test-input-cranfield/qrels.txt',
        '--topics', f'{_TEST_IO_DIR}/test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2', 'nDCG@2',
        '--output', f'{_TEST_OUTPUT_DIR}/test-output',
    ])
    shutil.rmtree(_TEST_IO_DIR / 'test-output', ignore_errors=True)
    verify(actual)
