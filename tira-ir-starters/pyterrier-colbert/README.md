docker build -t webis/tira-ir-starter-pyterrier-colbert:0.0.1 --build-arg MODEL_NAME=http://www.dcs.gla.ac.uk/~craigm/colbert.dnn.zip -f pyterrier-colbert/Dockerfile .

docker run --rm -ti \
	-v ${PWD}/tmp-out:/output \
	-v ${PWD}/clueweb-rerank:/input:ro \
	--entrypoint /reranking.py \
	webis/tira-ir-starter-pyterrier-colbert:0.0.1 \
	--input $inputDataset --output $outputDir

docker tag webis/tira-ir-starter-pyterrier-colbert:0.0.1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/colbert:0.0.1


/reranking.py --input $inputDataset --output $outputDir
