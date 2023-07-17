FROM webis/ir_measures_evaluator:dev-1.0.6

COPY ir_measures_evaluator.py /

COPY tests /tmp/tests/

RUN cd /tmp \
        && find -iname __pycache__ -exec rm -Rf {} \; || echo "" \
        && PYTHONPATH='../:.' pytest \
        && cd / \
        && rm -Rf /tmp/tests

ENTRYPOINT [ "/ir_measures_evaluator.py" ]
