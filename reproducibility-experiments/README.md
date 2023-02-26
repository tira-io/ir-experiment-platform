# Examples of Reproducibility Experiments

This directory exemplifies how archived reproducibility experiments on archived shared task repositories of the IR Experiment Platform look like.
This directory contains notebooks with detailed instructions and examples on how to do allow post-hoc experiments.
All examples work use the archived shared task of the 32 ir benchmarks on which we executed over 50 retrieval approaches: [https://github.com/tira-io/ir-experiment-platform-benchmarks](https://github.com/tira-io/ir-experiment-platform-benchmarks).

The reporucibility examples use jupyter notebooks.
To start them, please clone the archived shared task repository:

```
git clone git@github.com:tira-io/ir-experiment-platform-benchmarks.git
```

Inside the cloned repository, you can start the Jupyter notebook which automatically installs a minimal virtual environment using:
```
make jupyterlab
```


The installation of the environment is simplified with a virtual environment and executing `make jupyterlab` installs the virtual environment (if not already done) and starts the jupyter notebook ready to run all parts of the tutorial.

For each of the softwares submitted to TIRA, the `tira` integration to PyTerrier loads the Docker Image submitted to TIRA to execute it in PyTerrier pipelines (i.e., a first execution could take sligthly longer).

The following reproducibility notebooks are available:

- [full-rank-retriever-reproducibility.ipynb](full-rank-retriever-reproducibility.ipynb): showcases how full-rankers can be reproduced/replicated.
- [re-rank-reproducibility.ipynb](re-rank-reproducibility.ipynb): showcases how re-rankers can be reproduced/replicated.
- [interoparability-tutorial.ipynb](interoparability-tutorial.ipynb): showcases how full-rankers and re-rankers submitted in TIRA can be combined in new ways in post-hoc experiments.
