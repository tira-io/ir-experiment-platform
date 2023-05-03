# TIRA IR-Starter for MonoT5 in PyTerrier with Jupyter Notebooks

This directory contains a retrieval system that uses a Jupyter notebook with PyTerrier to rerank the top-1000 results of BM25 with MonoT5.
m.

## Local Development

Please use the `tira-run` command (can be installed via `pip3 install tira`) to test that your retrieval approach is correctly installed inside the Docker image.
For example, you can run the following command inside this directory to re-rank with an PyTerrier re-ranker from our tira-ir-starter with BM25 on a small example (2 queries from the passage retrieval task of TREC DL 2019):

```
tira-run \
    --input-directory ${PWD}/sample-input \
    --image webis/tira-ir-starter-pyterrier:0.0.1-base \
    --command '/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --params wmodel=BM25 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer'
```

In this example above, the command `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --params wmodel=BM25 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer` is the command that you would enter in TIRA, and the `--input-directory` flag points to the inputs.

This creates a run file `tira-output/run.txt`, with content like (`cat sample-output/run.txt |head -3`):

```
19335 Q0 8412684 1 2.0044117909904275 pyterrier.default_pipelines.wmodel_text_scorer
19335 Q0 8412687 2 1.6165480088144524 pyterrier.default_pipelines.wmodel_text_scorer
19335 Q0 527689 3 0.7777388572417481 pyterrier.default_pipelines.wmodel_text_scorer
```

Testing full-rank retrievers works analougously.

## Developing Retrieval Approaches in Declarative PyTerrier-Pipelines

The notebook [full-rank-pipeline.ipynb](full-rank-pipeline.ipynb) exemplifies how to directly run Jupyter Notebooks in TIRA.

You can run it locally via:

```
tira-run \
    --input-directory ${PWD}/sample-input-full-rank \
    --image webis/tira-ir-starter-pyterrier:0.0.1-base \
    --command '/workspace/run-pyterrier-notebook.py --input $inputDataset --output $outputDir --notebook /workspace/full-rank-pipeline.ipynb'
```

This creates a run file `tira-output/run.txt`, with content like (`cat sample-output/run.txt |head -3`):

```
1 0 pangram-03 1 -0.4919184192126373 BM25
1 0 pangram-01 2 -0.5271673505256447 BM25
1 0 pangram-04 3 -0.9838368384252746 BM25
```

## Submit the Image to TIRA

You need a team for your submission, in the following, we use `tira-ir-starter` as team name, to resubmit the image, please just replace `tira-ir-starter` with your team name.

First, you have to upload the image:

```
docker pull webis/tira-ir-starter-pyterrier-monot5:0.0.1-monot5-base-msmarco-10k

docker tag webis/tira-ir-starter-pyterrier-monot5:0.0.1-monot5-base-msmarco-10k registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pyterrier-monot5:0.0.1
docker push registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pyterrier-monot5:0.0.1
```

# Build the image

```
docker build --build-arg MODEL_NAME=castorini/monot5-base-msmarco-10k --build-arg TOKENIZER_NAME=t5-base -t webis/tira-ir-starter-pyterrier-monot5:0.0.1-monot5-base-msmarco-10k -f pyterrier-t5/Dockerfile .
```
