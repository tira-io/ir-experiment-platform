# TIRA IR-Starter for PyGaggle

This directory contains a retrieval system that uses [PyGaggle](https://github.com/castorini/pygaggle) models like monoBERT or monoT5 for retrieval.

Overall, this starter (or other versions derived from the starter) can serve as re-rank retrieval approaches following any previous retrieval stage.


## Local Development

Please use the `tira-run` command (can be installed via `pip3 install tira`) to test that your retrieval approach is correctly installed inside the Docker image.
For example, you can run the following command inside this directory to re-rank with an PyGaggle re-ranker from our tira-ir-starter on a small example (2 queries from the passage retrieval task of TREC DL 2019):

```
tira-run \
    --input-directory ${PWD}/sample-input \
    --image webis/tira-ir-starter-pygaggle:0.0.1-monot5-base-msmarco-10k \
    --command '/reranking.py --input $inputDataset --output $outputDir'
```

In this example above, the command `/reranking.py --input $inputDataset --output $outputDir` is the command that you would enter in TIRA, and the `--input-directory` flag points to the inputs.


This creates a run file `tira-output/run.txt`, with content like (`cat sample-output/run.txt |head -3`):

```
19335 0 8412684 1 -0.08743388205766678 castorini/monot5-base-msmarco-10k
19335 0 7267248 2 -0.20035237073898315 castorini/monot5-base-msmarco-10k
19335 0 527689 3 -0.9691352844238281 castorini/monot5-base-msmarco-10k
```

## Submit the Image to TIRA

You need a team for your submission, in the following, I use `tira-ir-starter` as team name, to resubmit the image, please just replace `tira-ir-starter` with your team name.

First, you have to upload the image:

```
docker pull webis/tira-ir-starter-pygaggle:0.0.1-monot5-large-msmarco-10k
docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-large-msmarco-10k registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-large-msmarco-10k
docker push registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-large-msmarco-10k
```

After the image is uploaded, you should use the following command in TIRA:

``` 
/reranking.py --input $inputDataset --output $outputDir
```

Please refer to the general tutorial on [how to import your retrieval approach to TIRA](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters#adding-your-retrieval-software) and on [how to run your retrieval software in TIRA](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters#running-your-retrieval-software) for more detailed instructions on how to submit.



## Building the images:

There are many different variants of the image, depending on the included monoT5 or monoBERT model.
All variants are:

```
docker build --build-arg MODEL_NAME=castorini/monot5-base-msmarco-10k --build-arg TOKENIZER_NAME=t5-base -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-base-msmarco-10k -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-base-msmarco-10k registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-base-msmarco-10k
```

```
docker build --build-arg MODEL_NAME=castorini/monot5-3b-msmarco --build-arg TOKENIZER_NAME=t5-3b -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-3b-msmarco -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-3b-msmarco registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-3b-msmarco
```

```
docker build --build-arg MODEL_NAME=castorini/monot5-large-msmarco --build-arg TOKENIZER_NAME=t5-large -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-large-msmarco -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-large-msmarco registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-large-msmarco
```

```
docker build --build-arg MODEL_NAME=castorini/monot5-large-msmarco-10k --build-arg TOKENIZER_NAME=t5-large -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-large-msmarco-10k -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-large-msmarco-10k registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-large-msmarco-10k
```

```
docker build --build-arg MODEL_NAME=castorini/monot5-base-med-msmarco --build-arg TOKENIZER_NAME=t5-base -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-base-med-msmarco -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-base-med-msmarco registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-base-med-msmarco
```

```
docker build --build-arg MODEL_NAME=castorini/monot5-small-msmarco-10k --build-arg TOKENIZER_NAME=t5-small -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-small-msmarco-10k -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-small-msmarco-10k registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-small-msmarco-10k
```

```
docker build --build-arg MODEL_NAME=castorini/monot5-small-msmarco-100k --build-arg TOKENIZER_NAME=t5-small -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-small-msmarco-100k -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-small-msmarco-100k registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-small-msmarco-100k
```

```
docker build --build-arg MODEL_NAME=castorini/monobert-large-msmarco-finetune-only --build-arg TOKENIZER_NAME=bert-large-uncased -t webis/tira-ir-starter-pygaggle:0.0.1-monobert-large-msmarco-finetune-only -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monobert-large-msmarco-finetune-only registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monobert-large-msmarco-finetune-only
```


You can test it locally via:
```
docker run --rm -ti \
	-v ${PWD}/tmp-out:/output \
	-v ${PWD}/clueweb-rerank:/input:ro \
	--entrypoint /reranking.py \
	webis/tira-ir-starter-pygaggle:0.0.1-monot5-base-msmarco-10k \
	--input $inputDataset --output $outputDir
```

```
docker build --build-arg MODEL_NAME=castorini/monobert-large-msmarco --build-arg TOKENIZER_NAME=bert-large-uncased -t webis/tira-ir-starter-pygaggle:0.0.1-monobert-large-msmarco -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monobert-large-msmarco registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monobert-large-msmarco
```

```
docker run --rm -ti \
	-v ${PWD}/tmp-out:/output \
	-v ${PWD}/clueweb-rerank:/input:ro \
	--entrypoint /reranking.py \
	webis/tira-ir-starter-pygaggle:0.0.1-monobert-large-msmarco \
	--input /input --output /output
```
