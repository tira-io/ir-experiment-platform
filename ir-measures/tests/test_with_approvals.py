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

from ir_measures_evaluator import main

_TEST_IO_DIR = Path(__file__).parent / 'test-io'


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
        # Copy test_io to temp_dir
        copytree(_TEST_IO_DIR, tmp_path)
        # Change to temp_dir
        os.chdir(tmp_path)
        # Override sys.argv
        sys.argv = ['', *argv]
        with redirect_stdout(buffer):
            if exit_normal:
                main()
            else:
                with raises(SystemExit):
                    main()
        # List files in temp output dir
        tmp_out_path = tmp_path / output_dir
        files = sorted(tmp_out_path.glob('**/*'))
        filenames = [
            str(file.relative_to(tmp_path)) for file in files
        ]
        captured_files += f'\n\n####\nfiles: {filenames}\n'
        for file in files:
            if not file.is_file():
                continue
            captured_files += f'\n\n####{file.relative_to(tmp_path)}\n' + \
                              open(file).read()
    return buffer.getvalue() + captured_files


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


def test_run_path_not_found():
    actual = _run_capture_stdout_files_fail([
        '--run', 'foo',
    ])
    verify(actual)


def test_run_path_is_dir():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input',
    ])
    verify(actual)


def test_run_file_empty():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/empty_file.txt',
    ])
    verify(actual)


def test_run_fewer_columns():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_invalid_less_columns.txt',
    ])
    verify(actual)


def test_run_more_columns():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_invalid_more_columns.txt',
    ])
    verify(actual)


def test_run_multiple_tags():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_invalid_multiple_tags.txt',
    ])
    verify(actual)


def test_run_tag_special_chars():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_tag_special_chars.txt',
    ])
    verify(actual)


def test_run_query_id_special_chars():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_qid_special_chars.txt',
    ])
    verify(actual)


def test_run_query_id_not_ascending():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_qid_not_asc.txt',
    ])
    verify(actual)


def test_run_document_id_special_chars():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_docid_special_chars.txt',
    ])
    verify(actual)


def test_run_ignored_column_not_default():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_ignored_column_wrong.txt',
    ])
    verify(actual)


def test_run_score_not_numeric():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_warning_score_not_num.txt',
    ])
    verify(actual)


def test_run_score_scientific_notation():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_score_scientific.txt',
    ])
    verify(actual)


def test_run_score_ties():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_score_ties.txt',
    ])
    verify(actual)


def test_run_score_not_descending():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_score_not_desc.txt',
    ])
    verify(actual)


def test_run_rank_not_numeric():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_warning_rank_not_num.txt',
    ])
    verify(actual)


def test_run_rank_not_integer():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_rank_not_int.txt',
    ])
    verify(actual)


def test_run_first_rank_not_zero():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_rank_not_start_at_0.txt',
    ])
    verify(actual)


def test_run_rank_ties():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_rank_ties.txt',
    ])
    verify(actual)


def test_run_rank_not_ascending():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_rank_not_asc.txt',
    ])
    verify(actual)


def test_run_rank_not_consecutive():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_rank_not_consecutive.txt',
    ])
    verify(actual)


def test_run_score_rank_inconsistent():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_consistency.txt',
    ])
    verify(actual)


def test_run_valid():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_valid.txt',
    ])
    verify(actual)


def test_qrels_path_not_found():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'bar',
        '--topics', 'test-input/topics_sample_valid.jsonl',
    ])
    verify(actual)


def test_qrels_path_is_dir():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input',
        '--topics', 'test-input/topics_sample_valid.jsonl',
    ])
    verify(actual)


def test_qrels_file_empty():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/empty_file.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
    ])
    verify(actual)


def test_qrels_valid_no_topics():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
    ])
    verify(actual)


def test_topics_path_not_found():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'baz',
    ])
    verify(actual)


def test_topics_path_is_dir():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input',
    ])
    verify(actual)


def test_topics_file_empty():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input/empty_file.jsonl',
    ])
    verify(actual)


def test_topics_valid_no_qrels():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
    ])
    verify(actual)


def test_qrels_topics_valid():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
    ])
    verify(actual)


def test_query_ids_inconsistent_run_qrels():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_qid_not_in_qrels.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
    ])
    verify(actual)


def test_document_ids_inconsistent_run_qrels():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_warning_docid_not_in_qrels.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
    ])
    verify(actual)


def test_query_ids_inconsistent_topics_run():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_valid.txt',
        '--topics', 'test-input/topics_sample_warning_qid_not_in_run.jsonl',
        '--qrels', 'test-input/qrels_sample_valid.txt',
    ])
    verify(actual)


def test_query_ids_inconsistent_topics_qrels():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_valid.txt',
        '--topics', 'test-input/topics_sample_warning_qid_not_in_qrels.jsonl',
        '--qrels', 'test-input/qrels_sample_valid.txt',
    ])
    verify(actual)


def test_measure_unknown():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
        '--measures', 'FOOBAR',
    ])
    verify(actual)


def test_measure_invalid():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
        '--measures', 'P@X',
    ])
    verify(actual)


def test_measure_valid_no_qrels():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2',
    ])
    verify(actual)


def test_measure_valid_no_topics():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--measures', 'P@2',
    ])
    verify(actual)


def test_measure_valid():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2',
    ])
    verify(actual)


def test_measures_valid():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2', 'nDCG@2',
    ])
    verify(actual)


def test_output_path_not_found():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2', 'nDCG@2',
        '--output', '42',
    ])
    verify(actual)


def test_output_path_is_file():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2', 'nDCG@2',
        '--output', 'test-output-not-empty/file.txt',
    ])
    verify(actual)


def test_output_dir_not_empty():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2', 'nDCG@2',
        '--output', 'test-output-not-empty',
    ], output_dir='test-output-not-empty')
    verify(actual)


def test_output_valid_no_qrels():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2', 'nDCG@2',
        '--output', 'test-output',
    ])
    verify(actual)


def test_output_valid_no_topics():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--measures', 'P@2', 'nDCG@2',
        '--output', 'test-output',
    ])
    verify(actual)


def test_output_valid_no_measures():
    actual = _run_capture_stdout_files_fail([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
        '--output', 'test-output',
    ])
    verify(actual)


def test_all_valid():
    actual = _run_capture_stdout_files_pass([
        '--run', 'test-input/run_sample_valid.txt',
        '--qrels', 'test-input/qrels_sample_valid.txt',
        '--topics', 'test-input/topics_sample_valid.jsonl',
        '--measures', 'P@2', 'nDCG@2',
        '--output', 'test-output',
    ])
    verify(actual)
