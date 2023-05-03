FROM webis/tira-ir-starter-pyterrier:0.0.1-base

RUN pip3 install --upgrade git+https://github.com/terrierteam/pyterrier_colbert.git \
	&& pip install faiss-gpu==1.6.3 \
	&& pip install tira==0.0.9

ARG MODEL_NAME=local
ENV MODEL_NAME ${MODEL_NAME}

RUN python3 -c "import pandas as pd; from tira.third_party_integrations import ensure_pyterrier_is_loaded; ensure_pyterrier_is_loaded(); from pyterrier_colbert.ranking import ColBERTFactory; colbert = ColBERTFactory('${MODEL_NAME}', '/tmp/tmp-index', 'index'); print(colbert.text_scorer()(pd.DataFrame([{'qid': '1', 'query': 'foo', 'docno': '1', 'text': 'bar'}])))"

COPY pyterrier-colbert/reranking.py /reranking.py

COPY pyterrier-colbert/bm25-colbert.ipynb /workspace/

RUN jupyter trust /workspace/*.ipynb

