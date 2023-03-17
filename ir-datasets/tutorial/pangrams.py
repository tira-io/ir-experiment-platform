import ir_datasets
from ir_datasets.formats import JsonlDocs, TrecXmlQueries, TrecQrels
from typing import NamedTuple, Dict
from ir_datasets.util.download import RequestsDownload
from ir_datasets.datasets.base import Dataset

DATASET_URL = 'https://raw.githubusercontent.com/tira-io/ir-experiment-platform/main/ir-datasets/tutorial/'

class PangramDocument(NamedTuple):
    doc_id: str
    text: str
    letters: int
    
    def default_text(self):
        return self.text

ir_datasets.registry.register('pangrams', Dataset(
    JsonlDocs(ir_datasets.util.Download([RequestsDownload(DATASET_URL + 'pangram-documents.jsonl')], expected_md5='3f67adc5d99a7b6b7a410d4aefc8fe3b'), doc_cls=PangramDocument, lang='en'),
    TrecXmlQueries(ir_datasets.util.Download([RequestsDownload(DATASET_URL + 'pangram-topics.xml')], expected_md5='411647769eabf8dbcaac85cdb734c50d'), lang='en'),
    TrecQrels(ir_datasets.util.Download([RequestsDownload(DATASET_URL + 'pangram-qrels.txt')], expected_md5='2ef82edf2e8c1f6724e92d9f422b3f5f'), {0: 'Not Relevant', 1: 'Relevant'})
))

