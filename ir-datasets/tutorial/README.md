# Tutorial: Import Custom `ir_datasets` to TIRA

This tutorial explains how new and custom datasets can be imported into TIRA via `ir_datasets`.
All datasets from the main branch of `ir_datasets` are supported by default, so that this tutorial shows how new, potentially work-in-progress data can be imported (making it still easy to merge the integration to the main branch of `ir_datasets` later).
Although this tutorial uses a tiny dataset that is publicly available in this directory (i.e., [pangram-documents.jsonl](pangram-documents.jsonl) and [pangram-topics.xml](pangram-topics.xml)), you dont have to make the data publicly available and you can also keep your code private in case your data is confidential.

## Requirements

This tutorial assumes that you have `Docker`, `git`, `python3`, and `tira` installed.

- Please use official documentation/tutorials to install `docker`, `git` and `python3` on your machine.
- Please run `pip3 install tira` to install the TIRA client library on your machine.

## Scenario

We want to build a hypothetical search engine for [pangrams](https://en.wikipedia.org/wiki/Pangram). A pangram is a sentence in which each letter of the alphabet occurs at least once. This tutorial first shows [how to integrate a new custom dataset](#how-to-integrate-a-new-custom-dataset) into ir_datasets, then it shows how [retrieval experiments](#retrieval-experiments) can be implemented to retrieve documents from this new dataset.

## How to integrate a new custom dataset

Retrieval experiments following the cranfield paradigm require a set of documents, a set of topics with information needs, and relevance judgments. To build and evaluate our hypothetical search engine for pangrams, we first collect the documents from an existing [list of pangrams](https://clagnut.com/blog/2380) and build a set of information needs for retrieval experiments. We assume that no relevance judgments are available yet (as they usually are created after "enough" retrieval models have been pooled).

### Documents

We use the JSON Lines text format to integrate a tiny corpus of pangrams into `ir_datasets` to allow for unified document access.
As corpus, we extract 5 pangrams from an existing [list of pangrams](https://clagnut.com/blog/2380).
Each pangram has a `doc_id`, its `text`, and a number of `letters` and we store this corpus in the file [pangram-documents.jsonl](pangram-documents.jsonl).

Our corpus in the file [pangram-documents.jsonl](pangram-documents.jsonl) is (e.g., run `cat pangram-documents.jsonl`):

```
{"doc_id": "pangram-01", "text": "How quickly daft jumping zebras vex.", "letters": 30}
{"doc_id": "pangram-02", "text": "Quick fox jumps nightly above wizard.", "letters":  31}
{"doc_id": "pangram-03", "text": "The jay, pig, fox, zebra and my wolves quack!", "letters": 33}
{"doc_id": "pangram-04", "text": "The quick brown fox jumps over the lazy dog.", "letters": 35}
{"doc_id": "pangram-05", "text": "As quirky joke, chefs won’t pay devil magic zebra tax.", "letters": 42}
```

### Topics

We use the TREC-XML format to specify two topics for our hypothetical pangram search engine.
Each topic describes an information need coming with a `title`, a `description`, and a `narrative` that we store in the file [pangram-topics.xml](pangram-topics.xml).

Our topics in the file [pangram-topics.xml](pangram-topics.xml) are (e.g., run `cat pangram-topics.xml`):

```
<topics>
  <topic number="1">
    <title>fox jumps above animal</title>
    <description>What pangrams have a fox jumping above some animal?</description>
    <narrative>Relevant pangrams have a fox jumping over an animal (e.g., an dog). Pangrams containing a fox that is not jumping or jumps over something that is not an animal are not relevant.</narrative>
  </topic>
  <topic number="2">
    <title>multiple animals including a zebra</title>
    <description>Which pangrams have multiple animals where one of the animals is a zebra?</description>
    <narrative>Relevant pangrams have at least two animals, one of the animals must be a Zebra. Pangrams containing only a Zebra are not relevant.</narrative>
  </topic>
</topics>
```

### Importing the new Dataset to TIRA

The python file [pangrams.py](pangrams.py) integrates our [documents](pangram-documents.jsonl) and [topics](pangram-topics.jsonl) into `ir_datasets`.

The `Dockerfile` embeds this `ir_datasets` integration into an Docker image suitable to import the data to TIRA.

Please build the Docker image via:

```
docker build -t pangram-ir-dataset .
```

To integrate this dataset to TIRA, we use the existing `/irds_cli.sh` script that is packaged in the image `pangram-dataset-tira` that we just have build. In TIRA, you have to specify the Docker image that contains the corresponding `ir_datasets` integration (e.g., the image that we just have build), and the import command that is executed in the container, which would be `/irds_cli.sh --ir_datasets_id pangrams --output_dataset_path $outputDir` in our case here.

We can test the integration to TIRA locally with `tira-run` (ensure this is installed via `pip3 install tira`).
Please execute the following command to import the data to a local directory `pangram-dataset-tira ` (TIRA would run the same command):

```
tira-run \
    --output-directory ${PWD}/pangram-dataset-tira \
    --image pangram-ir-dataset \
    --command '/irds_cli.sh --ir_datasets_id pangrams --output_dataset_path $outputDir'
```

This produces the unified files that approaches in TIRA would use as inputs in the directory `pangram-dataset-tira`, e.g., `documents.jsonl`, `metadata.json`, `queries.jsonl`, `queries.xml`, etc.

### Relevance Judgments

To go the full circle and evaluate retrieval approaches, we would need relevance judgments.
We skip this for the moment, as relevance judgments are typically only done after an experiment.

## Retrieval Experiments

Now that we have prepared our [documents](pangram-documents.jsonl) and [topics](pangram-topics.jsonl), we can do the actual retrieval.
In this tutorial, we will use a simple declarative PyTerrier pipeline defined in [../../tira-ir-starters/pyterrier/full-rank-pipeline.ipynb](../../tira-ir-starters/pyterrier/full-rank-pipeline.ipynb) that uses BM25 for retrieval that can be easily extended.

To run this `full-rank-pipeline.ipynb` notebook on our dataset exported to `pangram-dataset-tira`, please run:

```
tira-run \
    --input-directory ${PWD}/pangram-dataset-tira \
    --image webis/tira-ir-starter-pyterrier:0.0.1-base \
    --command '/workspace/run-pyterrier-notebook.py --input $inputDataset --output $outputDir --notebook /workspace/full-rank-pipeline.ipynb'
```

This creates a run file `tira-output/run.txt`, with content like (`cat tira-output/run.txt |head -3`):

```
1 0 pangram-03 1 -0.4919184192126373 BM25
1 0 pangram-01 2 -0.5271673505256447 BM25
1 0 pangram-04 3 -0.9838368384252746 BM25
```

For more details on the internals, please have a look at the [corresponding documentation of the PyTerrier starter](../../tira-ir-starters/pyterrier#developing-retrieval-approaches-in-declarative-pyterrier-pipelines).
