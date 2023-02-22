FROM webis/tira-ir-starter-pyterrier:0.0.1-base

RUN pip3 install --upgrade git+https://github.com/terrierteam/pyterrier_t5.git \
	&& pip install tira==0.0.9

ARG MODEL_NAME=local
ENV MODEL_NAME ${MODEL_NAME}

ARG TOKENIZER_NAME=local
ENV TOKENIZER_NAME ${TOKENIZER_NAME}

RUN python3 -c "from tira.third_party_integrations import ensure_pyterrier_is_loaded; ensure_pyterrier_is_loaded(); from pyterrier_t5 import DuoT5ReRanker; duo_t5 = DuoT5ReRanker(model='${MODEL_NAME}', tok_model='${TOKENIZER_NAME}');"

COPY pyterrier-duot5/reranking.py /reranking.py

