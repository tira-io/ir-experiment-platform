# The IR Experiment Platform

The Information Retrieval Experiment Platform integrates ir_datasets, ir_measures, and PyTerrier with TIRA to promote more standardized, reproducible, and scalable retrieval experiments---and ultimately blinded experiments in IR. Standardization is achieved when the input and output of an experiment are compatible with ir_datasets and ir_measures, and the retrieval approach implements PyTerrier’s interfaces. However, none of this is a must for reproducibility and scalability, as TIRA can run any dockerized software locally or remotely in a cloud-native execution environment. Version control and caching ensure efficient (re)execution. TIRA allows for blind evaluation when an experiment runs on a remote server/cloud not under the control of the experimenter. The test data and ground truth are then hidden from view, and the retrieval
software has to process them in a sandbox that prevents data leaks.

The platform currently includes 15 corpora (1.9 billion documents) on which 32 well-known shared tasks are based, as well as Docker images of 50 standard retrieval approaches. Within this setup, we were able to automatically run and evaluate the 50 approaches on the 32 tasks (1600 runs) in less than a week.

The hosted version of the IR Experiment Platform is open for submissions at [https://www.tira.io/task/ir-benchmarks](https://www.tira.io/task/ir-benchmarks).

## Submission

Submission is available at: The hosted version of the IR Experiment Platform is open for submissions at [https://www.tira.io/task/ir-benchmarks](https://www.tira.io/task/ir-benchmarks).

## Reproducibility

Examples of reproducibility experiments are available in the directory [reproducibility-experiments](reproducibility-experiments).
The main advantage of the IR Experiment Platform is that after the shared tasks, the complete shared task repository can be archived in a fully self contained archive (including all software, runs, etc.).
This repository [https://github.com/tira-io/ir-experiment-platform-benchmarks](https://github.com/tira-io/ir-experiment-platform-benchmarks) contains an archived shared task repository covering over 50~retrieval softwares on more than 32 benchmarks with overall over 2000 executed softwares.

## IR Starters

We provide starters for 4 frequently used IR research frameworks that can be used as basis for software submissions to the Information Retrieval Experiment Platform. Retrieval Systems submitted to the IR Experiment Platform has to be implemented in fully self-contained Docker images, i.e., the software must be able to run without internet connection to improve reproducibility (e.g., preventing cases where an external dependency or API is not available anymore in a few years). Our existing starters can be directly submitted to TIRA, as all of them have been extensively tested on 32 benchmarks in TIRA, and they also might serve as starting point for custom development.

The starters are available and documented in the directory [tira-ir-starters](tira-ir-starters).

### Starter for PyTerrier in Jupyter

The simplest starter implements BM25 retrieval using a few lines of declarative PyTerrier code in a Jupyter notebook.

