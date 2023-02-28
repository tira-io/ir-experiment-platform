FROM webis/tira-ir-starter-pyterrier:0.0.1-base

RUN pip3 install --no-deps chatnoir-pyterrier==2.0.5 && pip3 install --no-deps chatnoir_api && pip3 install dataclasses_json && pip3 uninstall -y tira && pip3 install tira==0.0.20

COPY chatnoir/chatnoir_pipelines.py chatnoir/retrieve-with-chatnoir.sh /workspace/

