FROM webis/tira-ir-baselines-pyterrier:0.0.1-base

ARG T5_TOKENIZER=local
ENV T5_TOKENIZER ${T5_TOKENIZER}

ARG T5_MODEL=local
ENV T5_MODEL ${T5_MODEL}

RUN pip install --upgrade git+https://github.com/terrierteam/pyterrier_t5.git \
	&& python3 -c "import pyterrier as pt; from pyterrier_t5 import MonoT5ReRanker, DuoT5ReRanker; DuoT5ReRanker(tok_model='${T5_TOKENIZER}', model='${T5_MODEL}');"

COPY pyterrier/full-rank-pipeline.ipynb pyterrier/retrieval-pipeline.ipynb pyterrier/run-pyterrier-notebook.py /workspace/

