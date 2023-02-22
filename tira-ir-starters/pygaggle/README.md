
docker build --build-arg MODEL_NAME=castorini/monot5-base-msmarco-10k --build-arg TOKENIZER_NAME=t5-base -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-base-msmarco-10k -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-base-msmarco-10k registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-base-msmarco-10k



docker build --build-arg MODEL_NAME=castorini/monot5-3b-msmarco --build-arg TOKENIZER_NAME=t5-3b -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-3b-msmarco -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-3b-msmarco registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-3b-msmarco


docker build --build-arg MODEL_NAME=castorini/monot5-large-msmarco --build-arg TOKENIZER_NAME=t5-large -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-large-msmarco -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-large-msmarco registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-large-msmarco



docker build --build-arg MODEL_NAME=castorini/monot5-large-msmarco-10k --build-arg TOKENIZER_NAME=t5-large -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-large-msmarco-10k -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-large-msmarco-10k registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-large-msmarco-10k



docker build --build-arg MODEL_NAME=castorini/monot5-base-med-msmarco --build-arg TOKENIZER_NAME=t5-base -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-base-med-msmarco -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-base-med-msmarco registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-base-med-msmarco


docker build --build-arg MODEL_NAME=castorini/monot5-small-msmarco-10k --build-arg TOKENIZER_NAME=t5-small -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-small-msmarco-10k -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-small-msmarco-10k registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-small-msmarco-10k



docker build --build-arg MODEL_NAME=castorini/monot5-small-msmarco-100k --build-arg TOKENIZER_NAME=t5-small -t webis/tira-ir-starter-pygaggle:0.0.1-monot5-small-msmarco-100k -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monot5-small-msmarco-100k registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monot5-small-msmarco-100k


docker build --build-arg MODEL_NAME=castorini/monobert-large-msmarco-finetune-only --build-arg TOKENIZER_NAME=bert-large-uncased -t webis/tira-ir-starter-pygaggle:0.0.1-monobert-large-msmarco-finetune-only -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monobert-large-msmarco-finetune-only registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monobert-large-msmarco-finetune-only




docker run --rm -ti \
	-v ${PWD}/tmp-out:/output \
	-v ${PWD}/clueweb-rerank:/input:ro \
	--entrypoint /reranking.py \
	webis/tira-ir-starter-pygaggle:0.0.1-monot5-base-msmarco-10k \
	--input $inputDataset --output $outputDir

/reranking.py --input $inputDataset --output $outputDir

docker build --build-arg MODEL_NAME=castorini/monobert-large-msmarco --build-arg TOKENIZER_NAME=bert-large-uncased -t webis/tira-ir-starter-pygaggle:0.0.1-monobert-large-msmarco -f pygaggle/Dockerfile.transformer .

docker tag webis/tira-ir-starter-pygaggle:0.0.1-monobert-large-msmarco registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pygaggle:0.0.1-monobert-large-msmarco

docker run --rm -ti \
	-v ${PWD}/tmp-out:/output \
	-v ${PWD}/clueweb-rerank:/input:ro \
	--entrypoint /reranking.py \
	webis/tira-ir-starter-pygaggle:0.0.1-monobert-large-msmarco \
	--input /input --output /output
