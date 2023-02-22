FROM webis/tira-ir-starter-pyterrier:0.0.1-base

RUN pip3 install --no-deps chatnoir-pyterrier && pip3 install --no-deps chatnoir_api && pip3 install dataclasses_json

COPY chatnoir/chatnoir_pipelines.py chatnoir/retrieve-with-chatnoir.sh /workspace/

