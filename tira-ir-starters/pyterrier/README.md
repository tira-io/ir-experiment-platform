# TIRA IR-Starter for PyTerrier

This directory contains a retrieval system that uses PyTerrier for full-rank and re-rank approaches.

Overall, this starter (or other versions derived from the starter) can run arbitrary declarative PyTerrier Pipelines, and we have executed 20 re-rank and 20 full-rank approaches (using BM25, PL2, etc. as retrieval models) on all benchmarks integrated into the platform.

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
docker pull webis/tira-ir-starter-pyterrier:0.0.1-base

docker tag webis/tira-ir-starter-pyterrier:0.0.1-base registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pyterrier:0.0.1
docker push registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pyterrier:0.0.1
```

The Full-Rank retriever for PyTerrier is intended to run in two stages, where the first stage builds the index, and the second stage retrieves from the index.
After the image is uploaded, you can define the first stage that builds the index via the following command in TIRA:

``` 
/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $outputDir
```

For the second stage that does the actual full-rank retrieval, you can specify all kinds of retrieval models available in PyTerrier, e.g.,:

- BM25: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=BM25 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DPH: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DPH --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- BM25+RM3: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=BM25 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve_rm3`

Similarly, the image can directly re-rank results, in which case no index is needed (i.e., it is only a single stage, not two stages). Again, you can specify all kinds of retrieval models available in PyTerrier as re-rankers, e.g.:

- BM25: `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=BM25 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DFIC: `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DFIC --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`


Please refer to the general tutorial on [how to import your retrieval approach to TIRA](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters#adding-your-retrieval-software) and on [how to run your retrieval software in TIRA](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters#running-your-retrieval-software) for more detailed instructions on how to submit.



## Building the image:

To build the image and to deploy it in TIRA, please run the follwoing commands:

```
docker build -t webis/tira-ir-starter-pyterrier:0.0.5-base -f pyterrier/Dockerfile.base .
docker push webis/tira-ir-starter-pyterrier:0.0.5-base
```




## Overview of all retrieval commands for TIRA:

- BM25: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=BM25 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- BM25+RM3: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=BM25 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve_rm3`
- BB2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=BB2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DFIC: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DFIC --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DFIZ: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DFIZ --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DFR_BM25: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DFR_BM25 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DFRee: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DFRee --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DFReeKLIM: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DFReeKLIM --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`

- DFRWeightingModel: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DFRWeightingModel --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DirichletLM: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DirichletLM --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DLH: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DLH --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DPH: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DPH --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- Hiemstra_LM: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=Hiemstra_LM --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`

- IFB2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=IFB2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- In_expB2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=In_expB2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- In_expC2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=In_expC2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- InB2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=InB2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- InL2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=InL2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`

- Js_KLs: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=Js_KLs --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- LGD: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=LGD --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- PL2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=PL2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- TF_IDF: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=TF_IDF --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- XSqrA_M: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=XSqrA_M --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`


## Overview of all Re-rank Commands for TIRA:

docker run --rm -ti -v ${PWD}/tmp-out:/output -v ${PWD}/clueweb-rerank:/input:ro --entrypoint /workspace/pyterrier_cli.py webis/tira-ir-starter-pyterrier:0.0.1-base --input /input --output /output --params wmodel=BM25 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer

docker run --rm -ti -v ${PWD}/tmp-out:/output -v ${PWD}/cranfield-rank:/input:ro --entrypoint /workspace/pyterrier_cli.py webis/tira-ir-starter-pyterrier:0.0.1-base --input /input --output /output --params wmodel=BM25 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer

docker run --rm -ti -v ${PWD}/tmp-out:/output -v ${PWD}/antique-rank:/input:ro --entrypoint /workspace/pyterrier_cli.py webis/tira-ir-starter-pyterrier:0.0.1-base --input /input --output /output --params wmodel=BM25 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer


- BM25 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=BM25 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DFIC Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DFIC --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DFIZ Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DFIZ --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DFR_BM25 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DFR_BM25 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DFRee Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DFRee --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DFReeKLIM Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DFReeKLIM --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DirichletLM Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DirichletLM --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DLH Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DLH --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DPH Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DPH --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- Hiemstra_LM Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=Hiemstra_LM --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- IFB2 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=IFB2 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- In_expB2 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=In_expB2 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- In_expC2 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=In_expC2 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- InB2 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=InB2 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- InL2 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=InL2 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- Js_KLs Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=Js_KLs --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- LGD Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=LGD --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- PL2 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=PL2 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- TF_IDF Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=TF_IDF --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- XSqrA_M Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=XSqrA_M --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`












