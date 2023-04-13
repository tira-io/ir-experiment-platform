# Tutorial: Import Custom `ir_datasets` to TIRA, do retrieval experiments, analyze the retrieval system's performance

This tutorial explains how new and custom datasets can be imported into TIRA via `ir_datasets`.
All datasets from the main branch of `ir_datasets` are supported by default, so that this tutorial shows how new, potentially work-in-progress data can be imported (making it still easy to merge the integration to the main branch of `ir_datasets` later).
Although this tutorial uses a tiny dataset that is publicly available in this directory (i.e., [pangram-documents.jsonl](pangram-documents.jsonl) and [pangram-topics.xml](pangram-topics.xml)), you dont have to make the data publicly available and you can also keep your code private in case your data is confidential.

## Requirements

This tutorial assumes that you have `Docker`, `git`, `python3`, and `tira` installed. If not:

- Please use official documentation/tutorials to install `docker`, `git` and `python3` on your machine.
- Please run `pip3 install tira` to install the TIRA client library on your machine.

## Preparation
Clone this repository and change to the directory containing this tutorial:

```
git clone git@github.com:tira-io/ir-experiment-platform.git
cd ir-experiment-platform/ir-datasets/tutorial
```

## Scenario

We want to build a hypothetical search engine for [pangrams](https://en.wikipedia.org/wiki/Pangram). A pangram is a sentence in which each letter of the alphabet occurs at least once. This tutorial first shows [how to integrate a new custom dataset](#how-to-integrate-a-new-custom-dataset) into ir_datasets, then it shows how [retrieval experiments](#retrieval-experiments) can be implemented to retrieve documents from this new dataset.

## Data – How to integrate a new custom dataset

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
    <narrative>Relevant pangrams have at least two animals, one of the animals must be a zebra. Pangrams containing only a zebra are not relevant.</narrative>
  </topic>
</topics>
```

### Importing the new Dataset to TIRA (dry run)

The python file [pangrams.py](pangrams.py) registers our [documents](pangram-documents.jsonl) and [topics](pangram-topics.jsonl) for use in `ir_datasets`. This means, our dataset is now locally available as a class. You do not have to execute this script now in this tutorial, but you can use it as a template when creating your own dataset later on.

The `Dockerfile` embeds this `ir_datasets` integration into a Docker image suitable to import the data to TIRA.

Please build the Docker image via:

```
docker build -t pangram-ir-dataset .
```

To integrate this dataset to TIRA, we use the script `/irds_cli.sh`, which is packaged in the image `pangram-dataset-tira` that we have just build. In TIRA, you have to specify the Docker image that contains the corresponding `ir_datasets` integration (e.g., the image that we just have build), and the import command that is executed in the container, which would be `/irds_cli.sh --ir_datasets_id pangrams --output_dataset_path $outputDir` in our case here.

We can test the integration to TIRA locally with `tira-run` (ensure this is installed via `pip3 install tira`).
Please execute the following command to import the data to a local directory `pangram-dataset-tira ` (TIRA would run the same command):

```
tira-run \
    --output-directory ${PWD}/pangram-dataset-tira \
    --image pangram-ir-dataset \
    --allow-network true \
    --command '/irds_cli.sh --ir_datasets_id pangrams --output_dataset_path $outputDir'
```

This produces the unified files that TIRA requires approaches to use as inputs. The files are saved to the directory `pangram-dataset-tira` and are named `documents.jsonl`, `metadata.json`, `queries.jsonl`, `queries.xml`. (Normally, as with other datasets, the files would also include relevance judgements, but we do not have them in this tutorial. This is because they are typically produced after an experiment has been run.)

## Methods – How to execute retrieval experiments

Now that we have prepared our [documents](pangram-documents.jsonl) and [topics](pangram-topics.jsonl), we can do the actual retrieval.
In this tutorial, we will use a simple declarative PyTerrier pipeline defined in [../../tira-ir-starters/pyterrier/full-rank-pipeline.ipynb](../../tira-ir-starters/pyterrier/full-rank-pipeline.ipynb) that uses BM25 for retrieval that can be easily extended in order to produce your own experiments later on.

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

## Analysis – How to analyze the retrieval system's performance

To cover the last step of frequent IR experiments, we have to analyse the results.
This tutorial covers both a qualitative and a quantitative analysis.

### Qualitative Analysis

The `pangram-ir-dataset` image that we created above already has a [diffir](https://github.com/capreolus-ir/diffir) integration (because this is already included in the starting point) to render run files for qualitative analysis in TIRA.

To render the run file produced above, please run:

```
tira-run \
    --input-directory ${PWD}/tira-output \
    --image pangram-ir-dataset \
    --allow-network true \
    --command 'diffir --dataset pangrams --web $outputDir/run.txt > $outputDir/run.html'
```

This creates a rendered run file `tira-output/run.html`, that looks like:

![Screenshot_20230317_113841](https://user-images.githubusercontent.com/10050886/225883358-064f3d60-9f06-4e74-96de-9aa0ed37ff4c.png)

### Quantitative Analysis

To make a quantitative analysis according to the Cranfield Paradigm, we need to judge query-document pairs.

We use the standard TREC-Qrels format to label the documents.
Each line in the qrels file has four entries `<QID> 0 <DOC_ID> <REL>` where `<QID>` is the id of the query, `<DOC_ID>` is the id of the document, and `<REL>` is the relevance label of the document for the query (e.g., if document `pangram-04` were the only document relevant to query 1, it would get a relevance label of 1 while all other documents for query 1 get a relevance label of 0).

Our relevance judgments in the file [pangram-qrels.txt](pangram-qrels.txt) are (e.g., run `cat pangram-qrels.txt`):


```
1 0 pangram-01 0
1 0 pangram-02 0
1 0 pangram-03 0
1 0 pangram-04 1
1 0 pangram-05 0
2 0 pangram-01 0
2 0 pangram-02 0
2 0 pangram-03 1
2 0 pangram-04 0
2 0 pangram-05 0
```

The `pangram-ir-dataset` image that we created above already has a [ir-measures](https://github.com/terrierteam/ir_measures) integration (because this is already included in the starting point) that we can use for evaluation. (When working with your own dataset you will need to install the ir_measures python package within the container.)


To evaluate the run file produced above in terms of nDCG@10, MRR, P@3, and Recall@3, please run:

```
tira-run \
    --input-directory ${PWD}/tira-output \
    --image pangram-ir-dataset \
    --allow-network true \
    --command 'ir_measures pangrams $outputDir/run.txt nDCG@10 MRR P@3 Recall@3'
```

This should output the following:

```
nDCG@10	0.5655
RR	0.4167
P@3	0.3333
R@3	1.0000
```

The TIRA evaluator (executed by TIRA) that makes some more checks for consistency in the run file would look like this:

```
tira-run \
    --input-directory ${PWD} \
    --input-run ${PWD}/.. \
    --image pangram-ir-dataset \
    --command '/ir_measures_evaluator.py --run ${inputRun}/tutorial/tira-output/run.txt --topics ${inputDataset}/pangram-dataset-tira/queries.jsonl --qrels ${inputDataset}/pangram-qrels.txt --output ${outputDir} --measures "P@10" "nDCG@10" "MRR"'
```

This creates the evaluation as above in a file `tira-output/evaluation.prototext` with content that should look like this:

```
measure {
	key: "P@10"
	value: "0.1"
}
measure {
	key: "RR"
	value: "0.41666666666666663"
}
measure {
	key: "nDCG@10"
	value: "0.5654648767857288"
}
```

# Additional Resources

- The [PyTerrier tutorial](https://github.com/terrier-org/ecir2021tutorial)
- The [PyTerrier documentation](https://pyterrier.readthedocs.io/en/latest/)
- The [TIRA quickstart](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters)


# Deploy this in TIRA

Prerequisities:

You have the docker image uploaded. E.g., by running:

```
docker tag pangram-ir-dataset webis/tira-ir-datasets-starter:0.0.45-pangram
docker push webis/tira-ir-datasets-starter:0.0.45-pangram
```
