docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-roberta-base-ance-firstp -t webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp -f beir/Dockerfile.dres .

docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-roberta-base-ance-firstp -t webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir-dres:0.0.1-msmarco-roberta-base-ance-firstp

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-roberta-base-ance-firstp-tira-docker-software-id-massive-passenger

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-roberta-base-ance-firstp-tira-docker-software-id-tough-schema



docker build --build-arg DRES_MODEL=msmarco-distilbert-base-v3 -t webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-base-v3 -f beir/Dockerfile.dres .
docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-base-v3 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-distilbert-base-v3


docker build --build-arg DRES_MODEL=msmarco-MiniLM-L6-cos-v5 -t webis/tira-ir-starter-beir:0.0.1-msmarco-MiniLM-L6-cos-v5 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-MiniLM-L6-cos-v5 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-MiniLM-L6-cos-v5


docker build --build-arg DRES_MODEL=msmarco-MiniLM-L12-cos-v5 -t webis/tira-ir-starter-beir:0.0.1-msmarco-MiniLM-L12-cos-v5 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-MiniLM-L12-cos-v5 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-MiniLM-L12-cos-v5


docker build --build-arg DRES_MODEL=msmarco-distilbert-cos-v5 -t webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-cos-v5 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-cos-v5 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-distilbert-cos-v5


docker build --build-arg DRES_MODEL=msmarco-bert-base-dot-v5 -t webis/tira-ir-starter-beir:0.0.1-msmarco-bert-base-dot-v5 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-bert-base-dot-v5 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-bert-base-dot-v5


docker build --build-arg DRES_MODEL=msmarco-distilbert-dot-v5 -t webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-dot-v5 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-dot-v5 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-distilbert-dot-v5


docker build --build-arg DRES_MODEL=msmarco-distilbert-base-tas-b -t webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-base-tas-b -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-msmarco-distilbert-base-tas-b registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-msmarco-distilbert-base-tas-b

docker build --build-arg DRES_MODEL=multi-qa-MiniLM-L6-cos-v1 -t webis/tira-ir-starter-beir:0.0.1-multi-qa-MiniLM-L6-cos-v1 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-multi-qa-MiniLM-L6-cos-v1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-multi-qa-MiniLM-L6-cos-v1


docker build --build-arg DRES_MODEL=multi-qa-distilbert-cos-v1 -t webis/tira-ir-starter-beir:0.0.1-multi-qa-distilbert-cos-v1 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-multi-qa-distilbert-cos-v1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-multi-qa-distilbert-cos-v1


docker build --build-arg DRES_MODEL=multi-qa-mpnet-base-cos-v1 -t webis/tira-ir-starter-beir:0.0.1-multi-qa-mpnet-base-cos-v1 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-multi-qa-mpnet-base-cos-v1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-multi-qa-mpnet-base-cos-v1


docker build --build-arg DRES_MODEL=multi-qa-MiniLM-L6-dot-v1 -t webis/tira-ir-starter-beir:0.0.1-multi-qa-MiniLM-L6-dot-v1 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-multi-qa-MiniLM-L6-dot-v1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-multi-qa-MiniLM-L6-dot-v1


docker build --build-arg DRES_MODEL=multi-qa-distilbert-dot-v1 -t webis/tira-ir-starter-beir:0.0.1-multi-qa-distilbert-dot-v1 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-multi-qa-distilbert-dot-v1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-multi-qa-distilbert-dot-v1


docker build --build-arg DRES_MODEL=multi-qa-mpnet-base-dot-v1 -t webis/tira-ir-starter-beir:0.0.1-multi-qa-mpnet-base-dot-v1 -f beir/Dockerfile.dres .

docker tag webis/tira-ir-starter-beir:0.0.1-multi-qa-mpnet-base-dot-v1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/beir:0.0.1-multi-qa-mpnet-base-dot-v1


/reranking.py --input $inputDataset --output $outputDir --score_function cos_sim



docker run --rm -ti \
	-v ${PWD}/tmp-out:/output \
	-v ${PWD}/clueweb-rerank:/input:ro \
	--entrypoint /reranking.py \
	webis/tira-ir-starter-beir:0.0.1-msmarco-roberta-base-ance-firstp \
	--input $inputDataset --output $outputDir --score_function cos_sim



	&& docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-distilbert-base-tas-b -t webis/tira-ir-baselines-beir:0.0.1-msmarco-distilbert-base-tas-b -f beir/Dockerfile.dres . \
	&& docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-distilbert-dot-v5 -t webis/tira-ir-baselines-beir:0.0.1-msmarco-distilbert-dot-v5 -f beir/Dockerfile.dres . \
	&& docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-bert-base-dot-v5 -t webis/tira-ir-baselines-beir:0.0.1-msmarco-bert-base-dot-v5 -f beir/Dockerfile.dres . \
