# TIRA IR-Starter for duoT5@PyTerrier

This directory contains a tira starter for the duoT5 retrieval model implemented in PyTerrier.

Overall, this starter (or other versions derived from the starter) can serve as re-rank retriever and we produce 3 different variants by switching out the embedded duoT5 model.

## Submit the Image to TIRA

You need a team for your submission, in the following, I use `tira-ir-starter` as team name, to resubmit the image, please just replace `tira-ir-starter` with your team name.

First, you have to upload the image:

```
docker pull webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco
docker tag webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco registry.webis.de/code-research/tira/tira-user-tira-ir-starter-duot5:0.0.1-duot5-base-msmarco
docker push registry.webis.de/code-research/tira/tira-user-tira-ir-starter-duot5:0.0.1-duot5-base-msmarco
```

After the image is uploaded, you should use the following command in TIRA:

``` 
/reranking.py --input $inputDataset --output $outputDir --top_k 25
```

Please refer to the general tutorial on [how to import your retrieval approach to TIRA](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters#adding-your-retrieval-software) and on [how to run your retrieval software in TIRA](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters#running-your-retrieval-software) for more detailed instructions on how to submit.



## Building the image:

To build the image and to deploy it in TIRA, please run the follwoing commands (we have 3 different variants, a full list comes below):

```
docker build --build-arg MODEL_NAME=castorini/duot5-base-msmarco --build-arg TOKENIZER_NAME=t5-base -t webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco -f pyterrier-duot5/Dockerfile .
docker push webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco
```



## Overview of all Images

```
docker build --build-arg MODEL_NAME=castorini/duot5-base-msmarco --build-arg TOKENIZER_NAME=t5-base -t webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco -f pyterrier-duot5/Dockerfile .

docker tag webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco registry.webis.de/code-research/tira/tira-user-tira-ir-starter/duot5:0.0.1-duot5-base-msmarco
```


```
docker build --build-arg MODEL_NAME=castorini/duot5-base-msmarco-10k --build-arg TOKENIZER_NAME=t5-base -t webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco-10k -f pyterrier-duot5/Dockerfile .

docker tag webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco-10k registry.webis.de/code-research/tira/tira-user-tira-ir-starter/duot5:0.0.1-duot5-base-msmarco-10k
```

```
docker build --build-arg MODEL_NAME=castorini/duot5-3b-msmarco --build-arg TOKENIZER_NAME=t5-3b -t webis/tira-ir-starter-duot5:0.0.1-duot5-3b-msmarco -f pyterrier-duot5/Dockerfile .

docker tag webis/tira-ir-starter-duot5:0.0.1-duot5-3b-msmarco registry.webis.de/code-research/tira/tira-user-tira-ir-starter/duot5:0.0.1-3b-msmarco
```

Run everything locally via:

```
docker run --rm -ti \
	-v ${PWD}/tmp-out:/output \
	-v ${PWD}/clueweb-rerank:/input:ro \
	--entrypoint /reranking.py \
	webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco \
	--input $inputDataset --output $outputDir --top_k 3
```
