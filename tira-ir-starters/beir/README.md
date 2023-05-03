# TIRA IR-Starter for Dense Retrievers in BEIR

This directory contains retrieval systems that dockerizes dense retrievers from [BEIR](https://github.com/beir-cellar/beir).
We obtain 17 different retrieval models by switching out the dense retrieval model (SBERT models) that can be used as re-ranker and as full-ranker.
For re-rankers, the approach uses a single stage (directly re-ranking all query-document pairs), and for full-ranking, this approach uses two stages (first stage indexes all documents into its dense vectors, the second stage does only the retrieval against the index).


## Local Development

Please use the `tira-run` command (can be installed via `pip3 install tira`) to test that your retrieval approach is correctly installed inside the Docker image.
For example, you can run the following command inside this directory to re-rank with an BEIR re-ranker from our tira-ir-starter on a small example (2 queries from the passage retrieval task of TREC DL 2019):

```
tira-run \
    --input-directory ${PWD}/sample-input \
    --image webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp \
    --command '/reranking.py --input $inputDataset --output $outputDir --score_function cos_sim'
```

In this example above, the command `/reranking.py --input $inputDataset --output $outputDir --score_function cos_sim` is the command that you would enter in TIRA, and the `--input-directory` flag points to the inputs.


This creates a run file `tira-output/run.txt`, with content like (`cat sample-output/run.txt |head -3`):

```
19335 0 8412684 1 0.9907888174057007 sentence-transformers/msmarco-roberta-base-ance-firstp-cos_sim
19335 0 7267248 2 0.9901072978973389 sentence-transformers/msmarco-roberta-base-ance-firstp-cos_sim
19335 0 527689 3 0.988582968711853 sentence-transformers/msmarco-roberta-base-ance-firstp-cos_si
```

We also have an jupyter notebook that allows for full-ranking.

```
tira-run \
    --input-directory ${PWD}/sample-input-full-rank \
    --image webis/tira-ir-starter-beir:0.0.2-msmarco-roberta-base-ance-firstp \
    --command '/full_ranking.py --input $inputDataset --output $outputDir --score_function cos_sim'
```

## Submit the Image to TIRA

You need a team for your submission, in the following, I use `tira-ir-starter` as team name, to resubmit the image, please just replace `tira-ir-starter` with your team name.

First, you have to upload the image:

```
docker pull webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp
docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp registry.webis.de/code-research/tira/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp
docker push registry.webis.de/code-research/tira/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp
```

After the image is uploaded, you should use the following command in TIRA:

``` 
/reranking.py --input $inputDataset --output $outputDir --score_function cos_sim
```

Please refer to the general tutorial on [how to import your retrieval approach to TIRA](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters#adding-your-retrieval-software) and on [how to run your retrieval software in TIRA](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters#running-your-retrieval-software) for more detailed instructions on how to submit.



## Building the image:

We produced 17 different variants of retrieval software by switching the included SBERT model. The images are build by commands like:

```
docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-roberta-base-ance-firstp -t webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp -f beir/Dockerfile.dres .
docker push webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp
```

The remaining variants are:

```
docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-roberta-base-ance-firstp -t webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp -f beir/Dockerfile.dres .
```

```
docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-roberta-base-ance-firstp -t webis/tira-ir-starter-beir:0.0.2-msmarco-roberta-base-ance-firstp -f beir/Dockerfile.dres .
```

```
docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-roberta-base-ance-firstp -t webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp -f beir/Dockerfile.dres .
```

```
docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir-dres:0.0.1-msmarco-roberta-base-ance-firstp
```

```
docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-roberta-base-ance-firstp-tira-docker-software-id-massive-passenger
```

```
docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-roberta-base-ance-firstp-tira-docker-software-id-tough-schema
```

```
docker build --build-arg DRES_MODEL=msmarco-distilbert-base-v3 -t webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-base-v3 -f beir/Dockerfile.dres .
docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-base-v3 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-distilbert-base-v3
```

```
docker build --build-arg DRES_MODEL=msmarco-MiniLM-L6-cos-v5 -t webis/tira-ir-starter-beir:0.0.1-msmarco-MiniLM-L6-cos-v5 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-MiniLM-L6-cos-v5 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-MiniLM-L6-cos-v5
```

```
docker build --build-arg DRES_MODEL=msmarco-MiniLM-L12-cos-v5 -t webis/tira-ir-starter-beir:0.0.1-msmarco-MiniLM-L12-cos-v5 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-MiniLM-L12-cos-v5 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-MiniLM-L12-cos-v5
```

```
docker build --build-arg DRES_MODEL=msmarco-distilbert-cos-v5 -t webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-cos-v5 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-cos-v5 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-distilbert-cos-v5
```

```
docker build --build-arg DRES_MODEL=msmarco-bert-base-dot-v5 -t webis/tira-ir-starter-beir:0.0.1-msmarco-bert-base-dot-v5 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-bert-base-dot-v5 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-bert-base-dot-v5
```

```
docker build --build-arg DRES_MODEL=msmarco-distilbert-dot-v5 -t webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-dot-v5 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-dot-v5 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-distilbert-dot-v5
```

```
docker build --build-arg DRES_MODEL=msmarco-distilbert-base-tas-b -t webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-base-tas-b -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-base-tas-b registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-distilbert-base-tas-b
```

```
docker build --build-arg DRES_MODEL=multi-qa-MiniLM-L6-cos-v1 -t webis/tira-ir-starter-beir:0.0.1-multi-qa-MiniLM-L6-cos-v1 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-multi-qa-MiniLM-L6-cos-v1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-multi-qa-MiniLM-L6-cos-v1
```

```
docker build --build-arg DRES_MODEL=multi-qa-distilbert-cos-v1 -t webis/tira-ir-starter-beir:0.0.1-multi-qa-distilbert-cos-v1 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-multi-qa-distilbert-cos-v1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-multi-qa-distilbert-cos-v1
```

```
docker build --build-arg DRES_MODEL=multi-qa-mpnet-base-cos-v1 -t webis/tira-ir-starter-beir:0.0.1-multi-qa-mpnet-base-cos-v1 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-multi-qa-mpnet-base-cos-v1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-multi-qa-mpnet-base-cos-v1
```

```
docker build --build-arg DRES_MODEL=multi-qa-MiniLM-L6-dot-v1 -t webis/tira-ir-starter-beir:0.0.1-multi-qa-MiniLM-L6-dot-v1 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-multi-qa-MiniLM-L6-dot-v1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-multi-qa-MiniLM-L6-dot-v1
```

```
docker build --build-arg DRES_MODEL=multi-qa-distilbert-dot-v1 -t webis/tira-ir-starter-beir:0.0.1-multi-qa-distilbert-dot-v1 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-multi-qa-distilbert-dot-v1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-multi-qa-distilbert-dot-v1
```

```
docker build --build-arg DRES_MODEL=multi-qa-mpnet-base-dot-v1 -t webis/tira-ir-starter-beir:0.0.1-multi-qa-mpnet-base-dot-v1 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-multi-qa-mpnet-base-dot-v1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-multi-qa-mpnet-base-dot-v1
```

You can run it via
```
/reranking.py --input $inputDataset --output $outputDir --score_function cos_sim
```

```
docker run --rm -ti \
	-v ${PWD}/tmp-out:/output \
	-v ${PWD}/clueweb-rerank:/input:ro \
	--entrypoint /reranking.py \
	webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp \
	--input $inputDataset --output $outputDir --score_function cos_sim
```

```
     docker ps
	&& docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-distilbert-base-tas-b -t webis/tira-ir-baselines-beir:0.0.1-msmarco-distilbert-base-tas-b -f beir/Dockerfile.dres . \
	&& docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-distilbert-dot-v5 -t webis/tira-ir-baselines-beir:0.0.1-msmarco-distilbert-dot-v5 -f beir/Dockerfile.dres . \
	&& docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-bert-base-dot-v5 -t webis/tira-ir-baselines-beir:0.0.1-msmarco-bert-base-dot-v5 -f beir/Dockerfile.dres . \
```
