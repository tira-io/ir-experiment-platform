FROM webis/tira-ir-datasets-starter:0.0.54

# The ir_datasets integration in "pangrams.py" and the resources "pangram-qrels.txt", "pangram-topics.xml", and "pangram-documents.jsonl" need to be
# located in a package "datasets_in_progress" on the pythonpath so that they can be found. The following copy command ensures this.
# You can test that it is correctly in the python path by running "from ir_datasets.datasets_in_progress import pangrams" inside a python shell.
# I.e., if your docker image has the name "pangram-ir-dataset" as in the tutorial, a command to test this would be:
# docker run --rm -ti --entrypoint  python3 pangram-ir-dataset -c 'from ir_datasets.datasets_in_progress import pangrams; help(pangrams)'
COPY pangrams.py pangram-qrels.txt pangram-topics.xml  pangram-documents.jsonl /usr/lib/python3.8/site-packages/ir_datasets/datasets_in_progress/

ENTRYPOINT [ "/irds_cli.sh" ]

