docker build --build-arg MODEL_NAME=castorini/duot5-base-msmarco --build-arg TOKENIZER_NAME=t5-base -t webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco -f pyterrier-duot5/Dockerfile .

docker tag webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco registry.webis.de/code-research/tira/tira-user-tira-ir-starter/duot5:0.0.1-duot5-base-msmarco


docker build --build-arg MODEL_NAME=castorini/duot5-base-msmarco-10k --build-arg TOKENIZER_NAME=t5-base -t webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco-10k -f pyterrier-duot5/Dockerfile .

docker tag webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco-10k registry.webis.de/code-research/tira/tira-user-tira-ir-starter/duot5:0.0.1-duot5-base-msmarco-10k


docker build --build-arg MODEL_NAME=castorini/duot5-3b-msmarco --build-arg TOKENIZER_NAME=t5-3b -t webis/tira-ir-starter-duot5:0.0.1-duot5-3b-msmarco -f pyterrier-duot5/Dockerfile .

docker tag webis/tira-ir-starter-duot5:0.0.1-duot5-3b-msmarco registry.webis.de/code-research/tira/tira-user-tira-ir-starter/duot5:0.0.1-3b-msmarco


castorini/duot5-base-msmarco-10k

docker run --rm -ti \
	-v ${PWD}/tmp-out:/output \
	-v ${PWD}/clueweb-rerank:/input:ro \
	--entrypoint /reranking.py \
	webis/tira-ir-starter-duot5:0.0.1-duot5-base-msmarco \
	--input $inputDataset --output $outputDir --top_k 3

/reranking.py --input $inputDataset --output $outputDir --top_k 25
