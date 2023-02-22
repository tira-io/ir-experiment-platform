FROM python:3.10

RUN pip3 install ir-measures approvaltests pytest

COPY ir_measures_evaluator.py /

COPY tests /tmp/tests/

RUN cd /tmp \
        && find -iname __pycache__ -exec rm -Rf {} \; || echo "" \
        && PYTHONPATH='../:.' pytest \
        && cd / \
        && rm -Rf /tmp/tests

ENTRYPOINT [ "/ir_measures_evaluator.py" ]
