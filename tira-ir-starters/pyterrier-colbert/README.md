# TIRA IR-Starter for ColBERT@PyTerrier

This directory contains a tira starter for the [ColBERT retrieval model implemented in PyTerrier](https://github.com/terrierteam/pyterrier_colbert).

Overall, this starter (or other versions derived from the starter) can serve as re-rank retriever and full-rank retriever (but we ommit the full-rank variant, as the indices become huge).

## Local Development

Please use the `tira-run` command (can be installed via `pip3 install tira`) to test that your retrieval approach is correctly installed inside the Docker image.
**Attention: ColBERT requires a GPU, i.e., ensure that you have installed the nvidia-runtime for Docker.**
For example, you can run the following command inside this directory to re-rank with an PyTerrier re-ranker from our tira-ir-starter with BM25 on a small example (2 queries from the passage retrieval task of TREC DL 2019):

```
tira-run \
    --input-directory ${PWD}/sample-input \
    --image webis/tira-ir-starter-pyterrier-colbert:0.0.1 \
    --command '/reranking.py --input $inputDataset --output $outputDir'
```

In this example above, the command `/reranking.py --input $inputDataset --output $outputDir` is the command that you would enter in TIRA, and the `--input-directory` flag points to the inputs.

## Submit the Image to TIRA

You need a team for your submission, in the following, I use `tira-ir-starter` as team name, to resubmit the image, please just replace `tira-ir-starter` with your team name.

First, you have to upload the image:

```
docker pull webis/tira-ir-starter-pyterrier-colbert:0.0.1
docker tag webis/tira-ir-starter-pyterrier-colbert:0.0.1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pyterrier-colbert:0.0.1
docker push registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pyterrier-colbert:0.0.1
```

After the image is uploaded, you should use the following command in TIRA:

``` 
/reranking.py --input $inputDataset --output $outputDir
```

Please refer to the general tutorial on [how to import your retrieval approach to TIRA](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters#adding-your-retrieval-software) and on [how to run your retrieval software in TIRA](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters#running-your-retrieval-software) for more detailed instructions on how to submit.



## Building the image:

```
docker build -t webis/tira-ir-starter-pyterrier-colbert:0.0.1 --build-arg MODEL_NAME=http://www.dcs.gla.ac.uk/~craigm/colbert.dnn.zip -f pyterrier-colbert/Dockerfile .
```

You can test it locally via:
```
docker run --rm -ti \
	-v ${PWD}/tmp-out:/output \
	-v ${PWD}/clueweb-rerank:/input:ro \
	--entrypoint /reranking.py \
	webis/tira-ir-starter-pyterrier-colbert:0.0.1 \
	--input $inputDataset --output $outputDir
```
