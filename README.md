# The IR Experiment Platform

The Information Retrieval Experiment Platform integrates ir_datasets, ir_measures, and PyTerrier with TIRA to promote more standardized, reproducible, and scalable retrieval experiments---and ultimately blinded experiments in IR. Standardization is achieved when the input and output of an experiment are compatible with ir_datasets and ir_measures, and the retrieval approach implements PyTerrier’s interfaces. However, none of this is a must for reproducibility and scalability, as TIRA can run any dockerized software locally or remotely in a cloud-native execution environment. Version control and caching ensure efficient (re)execution. TIRA allows for blind evaluation when an experiment runs on a remote server/cloud not under the control of the experimenter. The test data and ground truth are then hidden from view, and the retrieval
software has to process them in a sandbox that prevents data leaks.

The platform currently includes 15 corpora (1.9 billion documents) on which 32 well-known shared tasks are based, as well as Docker images of 50 standard retrieval approaches. Within this setup, we were able to automatically run and evaluate the 50 approaches on the 32 tasks (1600 runs) in less than a week.

The hosted version of the IR Experiment Platform is open for submissions at [https://www.tira.io/task/ir-benchmarks](https://www.tira.io/task/ir-benchmarks).

## Experiments

All evaluations and analysis (including those reported in the paper) are located in [analysis-of-submissions](analysis-of-submissions).

## Up-To-Date Leaderboards

Comparing the leaderboards accross different tasks is quite interesting (we have a large scale evaluation on that in the paper), e.g., compare [MS MARCO DL 2019](https://www.tira.io/task/ir-benchmarks#msmarco-passage-trec-dl-2019-judged-20230107-training) with [Antique](https://www.tira.io/task/ir-benchmarks#antique-test-20230107-training) or [Args.me](https://www.tira.io/task/ir-benchmarks#argsme-touche-2020-task-1-20230209-training): On MS MARCO, all kinds of deep learning models are at the top, which totally reverses for other corpora, e.g., Args.me or Antique.


The current leaderboards can be viewed in [tira.io](https://www.tira.io/task/ir-benchmarks):

- [Antique](https://www.tira.io/task/ir-benchmarks#antique-test-20230107-training)
- [Args.me 2020 Task 1](https://www.tira.io/task/ir-benchmarks#argsme-touche-2020-task-1-20230209-training)
- [Args.me 2021 Task 1](https://www.tira.io/task/ir-benchmarks#argsme-touche-2021-task-1-20230209-training)
- [Cranfield](https://www.tira.io/task/ir-benchmarks#cranfield-20230107-training)
- [TREC COVID](https://www.tira.io/task/ir-benchmarks#cord19-fulltext-trec-covid-20230107-training)
- [TREC Deep Learning 2019 (passage)](https://www.tira.io/task/ir-benchmarks#msmarco-passage-trec-dl-2019-judged-20230107-training)
- [TREC Deep Learning 2020 (passage)](https://www.tira.io/task/ir-benchmarks#msmarco-passage-trec-dl-2020-judged-20230107-training)
- [TREC Genomics 2004](https://www.tira.io/task/ir-benchmarks#medline-2004-trec-genomics-2004-20230107-training)
- [TREC Genomics 2005](https://www.tira.io/task/ir-benchmarks#medline-2004-trec-genomics-2005-20230107-training)
- [TREC 7](https://www.tira.io/task/ir-benchmarks#disks45-nocr-trec7-20230209-training)
- [TREC 8](https://www.tira.io/task/ir-benchmarks#disks45-nocr-trec8-20230209-training)
- [Robust04](https://www.tira.io/task/ir-benchmarks#disks45-nocr-trec-robust-2004-20230209-training)
- [TREC Web Track 2002 (gov)](https://www.tira.io/task/ir-benchmarks#gov-trec-web-2002-20230209-training)
- [TREC Web Track 2003 (gov)](https://www.tira.io/task/ir-benchmarks#gov-trec-web-2003-20230209-training)
- [TREC Web Track 2004 (gov)](https://www.tira.io/task/ir-benchmarks#gov-trec-web-2004-20230209-training)
- [TREC Web Track 2009 (ClueWeb09)](https://www.tira.io/task/ir-benchmarks#clueweb09-en-trec-web-2009-20230107-training)
- [TREC Web Track 2010 (ClueWeb09)](https://www.tira.io/task/ir-benchmarks#clueweb09-en-trec-web-2010-20230107-training)
- [TREC Web Track 2011 (ClueWeb09)](https://www.tira.io/task/ir-benchmarks#clueweb09-en-trec-web-2011-20230107-training)
- [TREC Web Track 2012 (ClueWeb09)](https://www.tira.io/task/ir-benchmarks#clueweb09-en-trec-web-2012-20230107-training)
- [TREC Web Track 2013 (ClueWeb12)](https://www.tira.io/task/ir-benchmarks#clueweb12-trec-web-2013-20230107-training)
- [TREC Web Track 2014 (ClueWeb12)](https://www.tira.io/task/ir-benchmarks#clueweb12-trec-web-2014-20230107-training)
- [Touché 2020 Task 2 (ClueWeb12)](https://www.tira.io/task/ir-benchmarks#clueweb12-touche-2020-task-2-20230209-training)
- [Touché 2021 Task 2 (ClueWeb12)](https://www.tira.io/task/ir-benchmarks#clueweb12-touche-2021-task-2-20230209-training)
- Touché 2023 Task 2 (ClueWeb22) ([Task is still ongoing](https://www.tira.io/task/touche-2023-task-2), so the leaderboard is not yet public)
- [TREC Terabyte 2004 (gov2)](https://www.tira.io/task/ir-benchmarks#gov2-trec-tb-2004-20230209-training)
- [TREC Terabyte 2005 (gov2)](https://www.tira.io/task/ir-benchmarks#gov2-trec-tb-2005-20230209-training)
- [TREC Terabyte 2006 (gov2)](https://www.tira.io/task/ir-benchmarks#gov2-trec-tb-2006-20230209-training)
- [NFCorpus](https://www.tira.io/task/ir-benchmarks#nfcorpus-test-20230107-training)
- [Vaswani](https://www.tira.io/task/ir-benchmarks#vaswani-20230107-training)
- [TREC Core 2018 (wapo)](https://www.tira.io/task/ir-benchmarks#wapo-v2-trec-core-2018-20230107-training)
- [TREC Precision Medicine 2017](https://www.tira.io/task/ir-benchmarks#medline-2017-trec-pm-2017-20230211-training)
- [TREC Precision Medicine 2018](https://www.tira.io/task/ir-benchmarks#medline-2017-trec-pm-2018-20230211-training)

## Import new Datasets

All datasets from the main branch of `ir_datasets` are supported by default.
We have a tutorial showing how new, potentially work-in-progress data can be imported at [ir-datasets/tutorial](ir-datasets/tutorial)

## Submission

Submission is available at: The hosted version of the IR Experiment Platform is open for submissions at [https://www.tira.io/task/ir-benchmarks](https://www.tira.io/task/ir-benchmarks). To simplify submissions, we provide several [starters](tira-ir-starters) (that yield 50 different retrieval models) that you can [use as starting point](tira-ir-starters).

After the run was unblinded and published by an organizer, it becomes visible on the leaderboard (here, as example, the top entries by nDCG@10 for the ClueWeb09):

![leaderboard-example](https://user-images.githubusercontent.com/10050886/221593767-fa405b12-2f46-4348-a036-43027000c882.png)



## Reproducibility

Examples of reproducibility experiments are available in the directory [reproducibility-experiments](reproducibility-experiments).
The main advantage of the IR Experiment Platform is that after the shared tasks, the complete shared task repository can be archived in a fully self contained archive (including all software, runs, etc.).
This repository [https://github.com/tira-io/ir-experiment-platform-benchmarks](https://github.com/tira-io/ir-experiment-platform-benchmarks) contains an archived shared task repository covering over 50~retrieval softwares on more than 32 benchmarks with overall over 2000 executed softwares.

## IR Starters

We provide starters for 4 frequently used IR research frameworks that can be used as basis for software submissions to the Information Retrieval Experiment Platform. Retrieval Systems submitted to the IR Experiment Platform has to be implemented in fully self-contained Docker images, i.e., the software must be able to run without internet connection to improve reproducibility (e.g., preventing cases where an external dependency or API is not available anymore in a few years). Our existing starters can be directly submitted to TIRA, as all of them have been extensively tested on 32 benchmarks in TIRA, and they also might serve as starting point for custom development.

The starters are available and documented in the directory [tira-ir-starters](tira-ir-starters).

### Starter for PyTerrier in Jupyter

The simplest starter implements BM25 retrieval using a few lines of declarative PyTerrier code in a Jupyter notebook.

