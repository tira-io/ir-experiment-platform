


build:
	docker build -t webis/tira-ir-baselines-beir:0.0.1-base -f beir/Dockerfile.base . \
	&& docker build --build-arg T5_TOKENIZER=t5-base --build-arg T5_MODEL=castorini/duot5-base-msmarco -t webis/tira-ir-baselines-duo-t5-preferences:0.0.1-castorini-duot5-base-msmarco -f duo-t5/Dockerfile . \
	&& docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-roberta-base-ance-firstp -t webis/tira-ir-baselines-beir:0.0.1-msmarco-roberta-base-ance-firstp -f beir/Dockerfile.dres . \
	&& docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-distilbert-base-tas-b -t webis/tira-ir-baselines-beir:0.0.1-msmarco-distilbert-base-tas-b -f beir/Dockerfile.dres . \
	&& docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-distilbert-dot-v5 -t webis/tira-ir-baselines-beir:0.0.1-msmarco-distilbert-dot-v5 -f beir/Dockerfile.dres . \
	&& docker build --build-arg DRES_MODEL=sentence-transformers/msmarco-bert-base-dot-v5 -t webis/tira-ir-baselines-beir:0.0.1-msmarco-bert-base-dot-v5 -f beir/Dockerfile.dres . \
	&& docker build -t webis/tira-ir-baselines-pygaggle:0.0.1-base -f pygaggle/Dockerfile.base . \
	&& docker build --build-arg MODEL_NAME=castorini/monot5-base-msmarco-10k --build-arg TOKENIZER_NAME=t5-base -t webis/tira-ir-baselines-pygaggle:0.0.1-monot5-base-msmarco-10k -f pygaggle/Dockerfile.transformer . \
	&& docker build -t webis/tira-ir-baselines-pyterrier:0.0.1-base -f pyterrier/Dockerfile.base . \




upload:
	docker tag webis/tira-ir-baselines-beir:0.0.1-msmarco-roberta-base-ance-firstp registry.webis.de/code-research/tira/tira-user-princess-knight/beir-dres-ance:0.0.1 \
	&& docker push registry.webis.de/code-research/tira/tira-user-princess-knight/beir-dres-ance:0.0.1 \
	&& docker tag webis/tira-ir-baselines-pygaggle:0.0.1-monot5-base-msmarco-10k registry.webis.de/code-research/tira/tira-user-princess-knight/pygaggle-monot5:0.0.1 \
	&& docker push registry.webis.de/code-research/tira/tira-user-princess-knight/pygaggle-monot5:0.0.1

run:
	docker run --rm -ti --cpus=2 -p 8888:8888 -v ${PWD}:/workspace webis/tira-ir-baselines-duo-t5-preferences:0.0.1-castorini-duot5-base-msmarco \
		jupyter-lab --allow-root --ip 0.0.0.0
#	docker run --rm -ti -v ${PWD}:/workspace webis/tira-ir-baselines-pygaggle:0.0.1-monot5-base-msmarco-10k \
#		/reranking.py --input_file dummy-tiny-input.jsonl
#	docker run --rm -ti -v ${PWD}:/workspace webis/tira-ir-baselines-beir:0.0.1-msmarco-roberta-base-ance-firstp \
#		/reranking.py --input_file dummy-tiny-input.jsonl --score_function dot

# TODOS BEIR:
#DPR: models.SentenceBERT(("facebook-dpr-question_encoder-multiset-base", "facebook-dpr-ctx_encoder-multiset-base", " [SEP] ")
#UseQA: models.UseQA("https://tfhub.dev/google/universal-sentence-encoder-qa/3")
#binary passage retriever:  models.BinarySentenceBERT("msmarco-distilbert-base-tas-b")
# Everything from: https://docs.google.com/spreadsheets/d/1L8aACyPaXrL8iEelJLGqlMqXKPX2oSP_R10pZoy77Ns/edit#gid=0

# TODOS PyGaggle:

# DuoT5: 'castorini/duot5-base-msmarco' +  't5-base'
# MonoBERT: 'castorini/monobert-large-msmarco' + 'bert-large-uncased'



