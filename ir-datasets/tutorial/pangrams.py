"""This python file registers a new ir_datasets class 'pangrams'.
   You can find the ir_datasets documentation here: https://github.com/allenai/ir_datasets/.
   This file is intended to work inside the Docker image produced during this tutorial (the Dockerfile copies it and the other files loaded below to the correct locations).
"""
import ir_datasets
from ir_datasets.formats import JsonlDocs, TrecXmlQueries, TrecQrels
from typing import NamedTuple, Dict
from ir_datasets.datasets.base import Dataset

class PangramDocument(NamedTuple):
    doc_id: str
    text: str
    letters: int
    
    def default_text(self):
        return self.text

ir_datasets.registry.register('pangrams', Dataset(
    JsonlDocs(ir_datasets.util.PackageDataFile(path='datasets_in_progress/pangram-documents.jsonl'), doc_cls=PangramDocument, lang='en'),
    TrecXmlQueries(ir_datasets.util.PackageDataFile(path='datasets_in_progress/pangram-topics.xml'), lang='en'),
    TrecQrels(ir_datasets.util.PackageDataFile(path='datasets_in_progress/pangram-qrels.txt'), {0: 'Not Relevant', 1: 'Relevant'})
))
