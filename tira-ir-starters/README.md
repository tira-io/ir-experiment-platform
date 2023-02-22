# TIRA IR Starters

We provide starters for 4 frequently used IR research frameworks that can be used as basis for software submissions to the Information Retrieval Experiment Platform. The simplest starter implements BM25 retrieval using a few lines of declarative PyTerrier code in a Jupyter notebook.

Retrieval Systems submitted to the IR Experiment Platform has to be implemented in fully self-contained Docker images, i.e., the software must be able to run without internet connection to improve reproducibility (e.g., preventing cases where an external dependency or API is not available anymore in a few years).

Our existing starters can be directly submitted to TIRA, as all of them have been extensively tested on 32 benchmarks in TIRA, and they also might serve as starting point for custom development.

## Available Starters

The following starters are available:

- [Dense Retrieval starters from BEIR](beir): 17 starters for modern bi-encoder approaches.
- [ChatNoir](chatnoir): BM25F retrieval via an REST API from huge corpora, such as the ClueWeb09, the ClueWeb12, or the ClueWeb22.
- [PyGaggle](pygaggle): 8 starters for cross-encoder models such as monoBERT or monoT5.
- [PyTerrier](pyterrier): 20 starters for lexical models such as BM25 or PL2.
- [DuoT5@PyTerrier](pyterrier-duot5): 3 starters using the DuoT5 approach implemented in the PyTerrier Plugin for DuoT5.
- [ColBERT@PyTerrier](pyterrier-colbert): Implementation of ColBERT in the PyTerrier Plugin.

