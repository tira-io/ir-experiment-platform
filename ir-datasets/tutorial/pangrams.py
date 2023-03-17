import ir_datasets
from ir_datasets.formats import JsonlDocs, TrecXmlQueries, TrecQrels
from typing import NamedTuple, Dict
from ir_datasets.util.download import RequestsDownload
from ir_datasets.datasets.base import Dataset

NAME = 'pangrams'
DOCS = 'https://raw.githubusercontent.com/tira-io/ir-experiment-platform/main/ir-datasets/tutorial/pangram-documents.jsonl'
QUERIES = 'https://raw.githubusercontent.com/tira-io/ir-experiment-platform/main/ir-datasets/tutorial/pangram-topics.xml'

class PangramDocument(NamedTuple):
    doc_id: str
    text: str
    letters: int
    
    def default_text(self):
        return self.text

def register_pangram_dataset():
    docs = JsonlDocs(ir_datasets.util.Download([RequestsDownload(DOCS)]), doc_cls=PangramDocument, lang='en')
    queries = TrecXmlQueries(ir_datasets.util.Download([RequestsDownload(QUERIES)]), lang='en')
    empty_qrels = TrecQrels(ir_datasets.util.Download([RequestsDownload(QUERIES)]), {})

    ir_datasets.registry.register(NAME, Dataset(docs, queries, empty_qrels))
    
register_pangram_dataset()

