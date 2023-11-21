#!/usr/bin/env python3

import argparse
import json
import os
import re
from pathlib import Path
from typing import Tuple, Dict, List, Optional
import gzip

import ir_measures
from ir_measures import Qrel, ScoredDoc, Measure, Metric
import sys
import pandas as pd


def add_error(
        error_log: Dict[str, Dict[str, List[str]]],
        key: str,
        line: int
) -> None:
    if key not in error_log['errors']:
        error_log['errors'][key] = []
    error_log['errors'][key].append(str(line))


def add_warning(
        error_log: Dict[str, Dict[str, List[str]]],
        key: str,
        line: int
) -> None:
    if key not in error_log['warnings']:
        error_log['warnings'][key] = []
    error_log['warnings'][key].append(str(line))


def print_error(message: str, indent: bool = True) -> None:
    tab = '\t' if indent else ''
    print(f'{tab}\N{Ballot X} {message}')


def print_warning(message: str, indent: bool = True) -> None:
    tab = '\t' if indent else ''
    print(f'{tab}\N{Warning Sign} {message}')


def print_success(message: str, indent: bool = True) -> None:
    tab = '\t' if indent else ''
    print(f'{tab}\N{Check Mark} {message}')


def print_info(message: str, indent: bool = True) -> None:
    tab = '\t' if indent else ''
    print(f'{tab}\N{Information Source} {message}')


def check_file_path(path: Path, target: str) -> None:
    print_info(f'Check {target} path: {path}', indent=False)
    target = target.capitalize()
    if not path.exists():
        print_error(f'{target} path does not exist.')
        print_error(f'{target} path is invalid: 1 error', indent=False)
        exit(1)
    if not path.is_file():
        print_error(f'{target} path is not a file.')
        print_error(f'{target} path is invalid: 1 error', indent=False)
        exit(1)
    if not os.access(path, os.R_OK):
        print_error(f'{target} file is not readable.')
        print_error(f'{target} path is invalid: 1 error', indent=False)
        exit(1)
    if path.stat().st_size <= 0:
        print_error(f'{target} file is empty.')
        print_error(f'{target} path is invalid: 1 error', indent=False)
        exit(1)
    print_success(f'{target} path is valid.', indent=False)


def check_output_path(path: Path, target: str) -> None:
    print_info(f'Check {target} path: {path}', indent=False)
    target = target.capitalize()
    if not path.exists():
        print_error(f'{target} path does not exist.')
        print_error(f'{target} path is invalid: 1 error', indent=False)
        exit(1)
    if not path.is_dir():
        print_error(f'{target} path is not a directory.')
        print_error(f'{target} path is invalid: 1 error', indent=False)
        exit(1)
    if not os.access(path, os.W_OK):
        print_error(f'{target} directory is not writable.')
        print_error(f'{target} path is invalid: 1 error', indent=False)
        exit(1)
    if next(path.iterdir(), None) is not None:
        print_warning(f'{target} directory is not empty.')
        print_success(f'{target} path is valid: 1 warning', indent=False)
    else:
        print_success(f'{target} path is valid.', indent=False)


def _is_number(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def _is_integer(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False


regexp_special_chars = re.compile(r'[^a-zA-Z0-9-_]+')


def check_run_file_content(path: Path) -> Dict[str, Dict[str, List[str]]]:
    error_log: Dict[str, Dict[str, List[str]]] = {
        'errors': {},
        'warnings': {},
    }

    with path.open('rt') as file:
        line_count = 1
        list_of_cols = []
        ignore_previous_cols = True

        lines = file.readlines()

        for line in lines:
            cols = line.rstrip().split()
            previous_cols = list_of_cols[-1] if list_of_cols else cols

            # check columns
            if len(cols) > 6:
                add_error(error_log, 'cols_more', line_count)
                ignore_previous_cols = True
            elif len(cols) < 6:
                add_error(error_log, 'cols_less', line_count)
                ignore_previous_cols = True
            else:
                # error_log everything column specific
                # only when the column count is correct
                # because otherwise the position of the data
                # is potentially corrupted

                # check tags
                if not cols[5] == previous_cols[5]:
                    add_error(error_log, 'tag_multi', line_count)
                if re.search(regexp_special_chars, cols[5]):
                    add_warning(error_log, 'tag_chars', line_count)

                # check query ids
                if re.search(regexp_special_chars, cols[0]):
                    add_warning(error_log, 'qid_chars', line_count)
                if cols[0] < previous_cols[0]:
                    add_warning(error_log, 'qid_asc', line_count)

                # check doc ids
                if re.search(regexp_special_chars, cols[2]):
                    add_warning(error_log, 'docid_chars', line_count)

                # check ignored column
                if not cols[1] == 'Q0':
                    add_warning(error_log, 'ignored_col', line_count)

                # check scores
                try:
                    float(cols[4])
                    float(previous_cols[4])

                    if 'e' in cols[4].lower():
                        add_warning(error_log, 'score_science', line_count)
                    if (
                            float(cols[4]) == float(previous_cols[4])
                            and not ignore_previous_cols
                    ):
                        add_warning(error_log, 'score_tied', line_count)
                    if float(cols[4]) > float(previous_cols[4]):
                        add_warning(error_log, 'score_desc', line_count)
                except:
                    if not _is_number(cols[4]):
                        add_error(error_log, 'score_num', line_count)
                    if (
                            cols[4] == previous_cols[4]
                            and not ignore_previous_cols
                    ):
                        add_warning(error_log, 'score_tied', line_count)
                    if cols[4] > previous_cols[4]:
                        add_warning(error_log, 'scor_desc', line_count)

                # check ranks
                if not _is_number(cols[3]):
                    add_error(error_log, 'rank_num', line_count)
                if not _is_integer(cols[3]):
                    add_warning(error_log, 'rank_int', line_count)
                else:
                    if line_count == 1 and int(cols[3]) != 0:
                        add_warning(error_log, 'rank_start', line_count)
                if cols[3] == previous_cols[3] and not ignore_previous_cols:
                    add_warning(error_log, 'rank_tied', line_count)
                if _is_integer(cols[3]) and _is_integer(previous_cols[3]):
                    if int(cols[3]) < int(previous_cols[3]):
                        add_warning(error_log, 'rank_asc', line_count)
                    if (
                            int(cols[3]) != int(previous_cols[3]) + 1
                            and line_count > 1 and not ignore_previous_cols
                    ):
                        add_warning(error_log, 'rank_consecutive', line_count)
                else:
                    if cols[3] < previous_cols[3]:
                        add_warning(error_log, 'rank_asc', line_count)

                # check consistency
                if _is_number(cols[4]) and _is_number(previous_cols[4]):
                    if _is_integer(cols[3]) and _is_integer(previous_cols[3]):
                        if (
                                (
                                        int(cols[3]) < int(previous_cols[3])
                                        and not float(cols[4]) > float(previous_cols[4]))
                                or
                                (
                                        float(cols[4]) > float(previous_cols[4])
                                        and not int(cols[3]) < int(previous_cols[3])
                                )
                        ):
                            add_warning(error_log, 'consistency', line_count)
                    else:
                        if (
                                (
                                        cols[3] < previous_cols[3]
                                        and not float(cols[4]) > float(previous_cols[4])
                                )
                                or
                                (
                                        float(cols[4]) > float(previous_cols[4])
                                        and not cols[3] < previous_cols[3]
                                )
                        ):
                            add_warning(error_log, 'consistency', line_count)
                else:
                    if _is_integer(cols[3]) and _is_integer(previous_cols[3]):
                        if (
                                (
                                        int(cols[3]) < int(previous_cols[3])
                                        and not cols[4] > previous_cols[4]
                                )
                                or
                                (
                                        cols[4] > previous_cols[4]
                                        and not cols[3] < previous_cols[3]
                                )
                        ):
                            add_warning(error_log, 'consistency', line_count)
                    else:
                        if (
                                (
                                        cols[3] < previous_cols[3]
                                        and not cols[4] > previous_cols[4]
                                )
                                or
                                (
                                        cols[4] > previous_cols[4]
                                        and not cols[3] < previous_cols[3]
                                )
                        ):
                            add_warning(error_log, 'consistency', line_count)

                            # at the end of iteration if columns are correct:
                # save actual line as previous line for the next iteration
                list_of_cols.append(cols)
                ignore_previous_cols = False
            # at the end of iteration: count line 
            line_count += 1

        return error_log


def check_consistency(
        run: List[ScoredDoc],
        qrels: List[Qrel],
        topics: List[dict],
) -> Dict[str, Dict[str, List[str]]]:
    run_queries = {scored_doc.query_id for scored_doc in run}
    run_docs = {scored_doc.doc_id for scored_doc in run}
    qrels_queries = {scored_doc.query_id for scored_doc in qrels}
    qrels_docs = {scored_doc.doc_id for scored_doc in qrels}
    topics_queries = {topic['qid'] for topic in topics}

    error_log: Dict[str, Dict[str, List[str]]] = {
        'errors': {},
        'warnings': {},
    }

    for query in sorted(run_queries):
        if query not in qrels_queries:
            add_warning(error_log, 'run_qid_qrels', query)

    for doc in sorted(run_docs):
        if doc not in qrels_docs:
            add_warning(error_log, 'run_docid_qrels', doc)

    for query in sorted(topics_queries):
        if query not in run_queries:
            add_warning(error_log, 'topics_qid_run', query)
        if query not in qrels_queries:
            add_warning(error_log, 'topics_qid_qrels', query)

    return error_log


def load_run(path: Path) -> List[ScoredDoc]:
    print_info('Load run with ir-measures.', indent=False)
    run = list(ir_measures.read_trec_run(str(path)))
    print_success(f'Run successfully loaded.', indent=False)
    return run


def load_qrels(path: Path) -> List[Qrel]:
    print_info('Load qrels with ir-measures.', indent=False)
    qrels = list(ir_measures.read_trec_qrels(str(path)))
    print_success(f'Qrels successfully loaded.', indent=False)
    return qrels


def load_topics(path: Path) -> List[dict]:
    print_info('Load topics.', indent=False)
    with path.open('rt') as lines:
        topics = [json.loads(line) for line in lines]
    print_success(f'Topics successfully loaded.', indent=False)
    return topics


def parse_measure_args(measures_str: List[str]) -> Optional[List[Measure]]:
    print_info(
        'Parse measures: '
        f'{", ".join(measures_str)}',
        indent=False
    )
    measures = []
    unknown = 0
    invalid = 0
    for measure_str in measures_str:
        try:
            measure = ir_measures.parse_measure(measure_str)
            measures.append(measure)
        except NameError:
            print_error(f'Measure is unknown: {measure_str}')
            unknown += 1
        except ValueError:
            print_error(f'Measure is invalid: {measure_str}')
            invalid += 1
    if invalid > 0 or unknown > 0:
        reasons = []
        if invalid > 0:
            reasons.append(f'{invalid} invalid')
        if unknown > 0:
            reasons.append(f'{unknown} unknown')
        print_error(f'Measures could not be parsed: {", ".join(reasons)}')
        exit(1)
    print_success(f'Measures successfully parsed.', indent=False)
    return measures


def evaluate(
        measures: list,
        qrels: List[Qrel],
        run: List[ScoredDoc],
) -> Tuple[Dict[Measure, float], List[Metric]]:
    print_info(
        f'Evaluate run with measures: '
        f'{", ".join([str(m) for m in measures])}',
        indent=False
    )
    aggregate_metrics = ir_measures.calc_aggregate(measures, qrels, run)
    query_metrics = list(ir_measures.iter_calc(measures, qrels, run))
    print_success(f'Run successfully evaluated.', indent=False)
    return aggregate_metrics, query_metrics


def write_aggregated_prototext(
        measure_metrics: Dict[Measure, float],
        path: Path,
) -> None:
    # Sort by measure name.
    metrics = (
        (str(measure), value)
        for measure, value in measure_metrics.items()
    )
    metrics = sorted(metrics, key=lambda item: item[0])
    with path.open('wt') as file:
        for index, (measure, value) in enumerate(metrics):
            file.write(
                f'measure {{\n'
                f'\tkey: "{measure}"\n'
                f'\tvalue: "{value}"\n'
                f'}}\n'
            )


def write_per_query_prototext(metrics: List[Metric], path: Path) -> None:
    numeric = all(metric.query_id.isnumeric() for metric in metrics)
    # Sort by measure name.
    metrics = sorted(
        metrics,
        key=lambda metric: str(metric.measure)
    )
    # Sort by query id.
    metrics = sorted(
        list(metrics),
        key=lambda metric: int(metric.query_id) if numeric else metric.query_id
    )
    with path.open('wt') as file:
        for index, metric in enumerate(metrics):
            file.write(
                f'measure {{\n'
                f'\tquery_id: "{metric.query_id}"\n'
                f'\tmeasure: "{metric.measure}"\n'
                f'\tvalue: "{metric.value}"\n'
                f'}}\n'
            )


def parse_args():
    parser = argparse.ArgumentParser(
        description='Evaluate submissions with ir-measures.'
    )
    parser.add_argument(
        '--run',
        type=Path,
        help='Run in TREC format.',
        required=True,
    )
    parser.add_argument(
        '--qrels',
        type=Path,
        help='Qrels in TREC format. '
             'If no qrels are provided, only the run file is validated.',
        required=False,
    )
    parser.add_argument(
        '--topics',
        type=Path,
        help='Topics in JSON-Lines format. '
             'If no topics are provided, only the run file is validated.',
        required=False,
    )
    parser.add_argument(
        '--measures',
        type=str,
        nargs='+',
        help='Measure(s) to evaluate.',
        required=False,
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output path for the prototext file with evaluation results.',
        required=False,
    )
    return parser.parse_args()


def _error_count(error_log: Dict[str, Dict[str, List[str]]]) -> int:
    return sum(len(errors) for errors in error_log['errors'].values())


def _warnings_count(error_log: Dict[str, Dict[str, List[str]]]) -> int:
    return sum(len(warnings) for warnings in error_log['warnings'].values())


def check_run_format(run_path: Path) -> None:
    print_info(f'Check run file format.', indent=False)
    run_error_log = check_run_file_content(run_path)

    if _error_count(run_error_log):
        for key, value in run_error_log['errors'].items():

            more = f'(+{str(len(value) - 5)} more)' \
                if (len(value) - 5) > 0 else ''

            if key == 'cols_more':
                print_error(
                    f'More then 6 columns at lines: '
                    f'{", ".join(value[:5])} {more}'
                )
            if key == 'cols_less':
                print_error(
                    f'Fewer then 6 columns at lines: '
                    f'{", ".join(value[:5])} {more}'
                )
            if key == 'score_num':
                print_error(
                    f'Non-numeric scores at lines: '
                    f'{", ".join(value[:5])} {more}'
                )
            if key == 'rank_num':
                print_error(
                    f'Non-numeric ranks at lines: '
                    f'{", ".join(value[:5])} {more}'
                )
            if key == 'tag_multi':
                lines = [
                    f'{int(line) - 1}≠{line}'
                    for line in value[:5]
                ]
                print_error(
                    f'Conflicting run tags at lines: '
                    f'{", ".join(lines)} {more}'
                )

    if _warnings_count(run_error_log):
        for key, value in run_error_log['warnings'].items():

            more = f'(+{str(len(value) - 5)} more)' \
                if (len(value) - 5) > 0 else ''

            if key == 'tag_chars':
                print_warning(
                    f'Run tags with special characters at lines: '
                    f'{", ".join(value[:5])} {more}'
                )
            if key == 'qid_chars':
                print_warning(
                    f'Query IDs with special characters at lines: '
                    f'{", ".join(value[:5])} {more}'
                )
            if key == 'qid_asc':
                lines = [
                    f'{int(line) - 1}>{line}'
                    for line in value[:5]
                ]
                print_warning(
                    f'Query IDs not in ascending order at lines: '
                    f'{", ".join(lines)} {more}'
                )
            if key == 'docid_chars':
                print_warning(
                    f'Document IDs with special characters at lines: '
                    f'{", ".join(value[:5])} {more}'
                )
            if key == 'ignored_col':
                print_warning(
                    f'Ignored column is not "Q0" at lines: '
                    f'{", ".join(value[:5])} {more}'
                )
            if key == 'score_science':
                print_warning(
                    f'Score in scientific notation at lines: '
                    f'{", ".join(value[:5])} {more}'
                )
            if key == 'score_tied':
                lines = [
                    f'{int(line) - 1}={line}'
                    for line in value[:5]
                ]
                print_warning(
                    f'Scores ties at lines: '
                    f'{", ".join(lines)} {more}'
                )
            if key == 'score_desc':
                lines = [
                    f'{int(line) - 1}<{line}'
                    for line in value[:5]
                ]
                print_warning(
                    f'Scores not in descending order at lines: '
                    f'{", ".join(lines)} {more}'
                )
            if key == 'rank_int':
                print_warning(
                    f'Non-integer ranks at lines: '
                    f'{", ".join(value[:5])} {more}'
                )
            if key == 'rank_start':
                print_warning(f'Ranks do not start at 0.')
            if key == 'rank_tied':
                lines = [
                    f'{int(line) - 1}={line}'
                    for line in value[:5]
                ]
                print_warning(
                    f'Rank ties at lines: '
                    f'{", ".join(lines)} {more}'
                )
            if key == 'rank_asc':
                lines = [
                    f'{int(line) - 1}>{line}'
                    for line in value[:5]
                ]
                print_warning(
                    f'Ranks not in ascending order at lines: '
                    f'{", ".join(lines)} {more}'
                )
            if key == 'rank_consecutive':
                lines = [
                    f'{int(line) - 1}↛{line}'
                    for line in value[:5]
                ]
                print_warning(
                    f'Ranks not consecutive at lines: '
                    f'{", ".join(lines)} {more}'
                )
            if key == 'consistency':
                lines = [
                    f'{int(line) - 1}≷{line}'
                    for line in value[:5]
                ]
                print_warning(
                    f'Ranks and scores inconsistent at lines: '
                    f'{", ".join(lines)} {more}'
                )

    if _error_count(run_error_log):
        warn_str = ''
        if _warnings_count(run_error_log):
            warn_str = f', {_warnings_count(run_error_log)} warnings'
        print_error(
            f'Run file format is invalid: '
            f'{_error_count(run_error_log)} errors{warn_str}',
            indent=False
        )
        exit(1)
    elif _warnings_count(run_error_log):
        print_warning(
            f'Run file format is valid: '
            f'{_warnings_count(run_error_log)} warnings',
            indent=False
        )
    else:
        print_success(f'Run file format is valid.', indent=False)


def check_run_consistency(
        run: List[ScoredDoc],
        qrels: List[Qrel],
        topics: List[dict],
) -> None:
    print_info('Check run, qrels, and topics consistency.', indent=False)
    consistency_error_log = check_consistency(run, qrels, topics)
    if _warnings_count(consistency_error_log):
        for key, value in consistency_error_log['warnings'].items():

            more = f'(+{str(len(value) - 5)} more)' \
                if (len(value) - 5) > 0 else ''

            if key == 'run_qid_qrels':
                print_warning(
                    f'Query IDs of run file not found in qrels file: '
                    f'{", ".join(value[:5])} {more}'
                )
            if key == 'run_docid_qrels':
                print_warning(
                    f'Document IDs of run file not found in qrels file: '
                    f'{", ".join(value[:5])} {more}'
                )
            if key == 'topics_qid_run':
                print_warning(
                    f'Query IDs of topics file not found in run file: '
                    f'{", ".join(value[:5])} {more}'
                )
            if key == 'topics_qid_qrels':
                print_warning(
                    f'Query IDs of topics file not found in qrels file: '
                    f'{", ".join(value[:5])} {more}'
                )
        print_warning(
            f'Run, qrels, and topics are inconsistent: '
            f'{_warnings_count(consistency_error_log)} warnings',
            indent=False
        )
    else:
        print_success(
            f'Run, qrels, and topics are consistent.',
            indent=False
        )


def write_prototext(
        aggregated: Dict[Measure, float],
        per_query: List[Metric],
        output_path: Path,
) -> None:
    print_info('Export metrics.', indent=False)
    write_aggregated_prototext(
        aggregated,
        output_path / "evaluation.prototext"
    )
    write_per_query_prototext(
        per_query,
        output_path / "evaluation-per-query.prototext"
    )
    print_success('Metrics successfully exported.', indent=False)


def main():
    # Parse command line arguments.
    args = parse_args()

    # Check run file.
    run_path = args.run
    if run_path is not None:
        # Check and load run.
        check_file_path(run_path, 'run')
        check_run_format(run_path)
        run = load_run(run_path)
    else:
        run = None

    # Check qrels.
    qrels_path = args.qrels
    if qrels_path is not None:
        # Check and load qrels.
        check_file_path(qrels_path, 'qrels')
        qrels = load_qrels(qrels_path)
    else:
        qrels = None

    # Check topic.
    topics_path = args.topics
    if topics_path is not None:
        # Check and load topics.
        check_file_path(topics_path, 'topics')
        topics = load_topics(topics_path)
    else:
        topics = None

    # Check measures.
    measures_str = args.measures
    if measures_str is not None:
        # Check and load measures.
        measures = parse_measure_args(measures_str)
    else:
        measures = None

    # Check output path.
    output_path = args.output
    if output_path is not None:
        check_output_path(output_path, 'output')

    # Shortcuts for early exit.
    if run is None:
        print_error('Unable to validate without run file.', indent=False)
        exit(1)

    if qrels is None or topics is None:
        if qrels is not None:
            # Must have qrels and topics or neither.
            print_error(
                'Consistency check without topics file is not allowed.',
                indent=False
            )
            exit(1)
        if topics is not None:
            # Must have qrels and topics or neither.
            print_error(
                'Consistency check without qrels file is not allowed.',
                indent=False
            )
            exit(1)
        missing = []
        if qrels is None:
            missing.append('qrels')
        if topics is None:
            missing.append('topics')
        if measures is not None:
            print_error(
                f'Measuring without {" and ".join(missing)} files '
                f'is not allowed.',
                indent=False
            )
            exit(1)
        if output_path is not None:
            print_error(
                f'Exporting metrics without {" and ".join(missing)} files '
                f'is not allowed.',
                indent=False
            )
            exit(1)
        # Only check run format, no consistency check.
        return

    # Check run, qrels, and topics consistency.
    check_run_consistency(run, qrels, topics)

    # Shortcuts for early exit.
    if measures is None:
        if output_path is not None:
            print_error(
                'Exporting metrics without measures is not allowed.',
                indent=False
            )
            exit(1)
        # Only consistency check, no measurement.
        return

    aggregated, per_query = evaluate(measures, qrels, run)

    # Shortcuts for early exit.
    if output_path is None:
        # Only measure, no writing to output.
        return

    write_prototext(aggregated, per_query, output_path)

    irds_id = irds_id_from_metadata_or_none(args.qrels)
    if irds_id:
        try:
            render_results(args.run, irds_id, output_path)
        except Exception as e:
            pass


def normalized_run(run, depth=1000):
    run = pd.read_csv(run, sep="\s+", names=["qid", "q0", "docno", "rank", "score", "system"])

    try:
        run['qid'] = run['qid'].astype(int)
    except:
        pass

    run = run.copy().sort_values(["qid", "score", "docno"], ascending=[True, False, False]).reset_index()

    if 'Q0' not in run.columns:
        run['Q0'] = 0

    run = run.groupby("qid")[["qid", "Q0", "docno", "score", "system"]].head(depth)

    # Make sure that rank position starts by 1
    run["rank"] = 1
    run["rank"] = run.groupby("qid")["rank"].cumsum()
    
    return run[['qid', 'Q0', 'docno', 'rank', 'score', 'system']]

def queries_dict(irds_dataset):
    return {str(i.query_id): i for i in irds_dataset.queries_iter()}

def qrels_dict(irds_dataset):
    ret = {}

    for qrel in irds_dataset.qrels_iter():
        qid = str(qrel.query_id)
        if qid not in ret:
            ret[qid] = {}
        ret[qid][str(qrel.doc_id)] = qrel.relevance
    
    return ret

def render_results(run_file, irds_id, output_path, top_k=10):
    sys.path.append('/tira/application/src/tira/')
    import ir_datasets
    from ir_datasets_loader import IrDatasetsLoader
    irds_loader = IrDatasetsLoader()
    dataset = ir_datasets.load(irds_id)
    all_queries = queries_dict(dataset)
    all_qrels = qrels_dict(dataset)

    docs_store = dataset.docs_store()
    excerpt_for_rendering = {'queries': {}, 'documents': {}, 'qrels': {}}

    run = normalized_run(run_file, top_k)

    for _, i in run.iterrows():
        qid = str(i.qid)
        docno = str(i.docno)
        excerpt_for_rendering['queries'][qid] = all_queries[qid]
        excerpt_for_rendering['documents'][docno] = docs_store.get(docno)

        if qid in all_qrels and docno in all_qrels[qid]:
            if qid not in excerpt_for_rendering['qrels']:
                excerpt_for_rendering['qrels'][qid] = {}
            excerpt_for_rendering['qrels'][qid][docno] = all_qrels[qid][docno]

    excerpt_for_rendering['queries'] = {k: json.loads(irds_loader.map_query_as_jsonl(v)) for k,v in excerpt_for_rendering['queries'].items()}
    excerpt_for_rendering['documents'] = {k: json.loads(irds_loader.map_doc(v)) for k,v in excerpt_for_rendering['documents'].items()}

    with gzip.open(Path(output_path) / '.data-top-10-for-rendering.json.gz', 'wt') as output_file:
        output_file.write(json.dumps(excerpt_for_rendering))


def irds_id_from_metadata_or_none(f):
    try:
        f = Path(f)
        for p in [f / 'metadata.json', f.parent / 'metadata.json']:
            if (p).is_file():
                return json.load(open(p))['ir_datasets_id']
    except:
        pass


if __name__ == '__main__':
    main()
