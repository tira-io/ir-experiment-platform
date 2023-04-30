FROM webis/tira-ir-datasets-starter:0.0.54

COPY pangrams.py pangram-qrels.txt pangram-topics.xml  pangram-documents.jsonl /usr/lib/python3.8/site-packages/ir_datasets/datasets_in_progress/

ENTRYPOINT [ "/irds_cli.sh" ]

