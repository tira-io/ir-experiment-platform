# TIRA IR-Starter for ChatNoir

This directory contains a retrieval system that uses the REST API of ChatNoir to retrieve documents from large corpora such as the ClueWeb09, the ClueWeb12, or the ClueWeb22.
ChatNoir is reachable from within TIRA, and we keep the REST API of ChatNoir compatible to ensure reproducibility over the years.

Overall, this starter (or other versions derived from the starter, maybe with custom Query Expansion or similar) can serve as full-rank retriever against huge corpora.
TIRA injects the to-be-used credentials (i.e., the API key and index) in a configuration file, so that an approach can run in multiple shared tasks.

## Local Development

Please use the `tira-run` command (can be installed via `pip3 install tira`) to test that your retrieval approach is correctly installed inside the Docker image.
For example, you can run the following command inside this directory to retrieve with the ChatNoir retrieval model from our tira-ir-starter on a small example (using the first 3 queries of the TREC Web Track 2009):

```
tira-run \
    --input-directory ${PWD}/sample-input \
    --image webis/tira-ir-starter-chatnoir:0.0.2 \
    --command '/workspace/retrieve-with-chatnoir.sh --input $inputDataset --output $outputDir'
```

In this example above, the command `/workspace/retrieve-with-chatnoir.sh --input $inputDataset --output $outputDir` is the command that you would enter in TIRA, and the `--input-directory` flag points to the inputs.

This creates a run file `tira-output/run.txt`, with content like (`cat sample-output/run.txt |head -3`):

```
1 Q0 clueweb09-en0044-22-32198 1 1811.187 pyterrier.chatnoir_pipelines.retrieve_by_default_text
1 Q0 clueweb09-en0059-35-02945 2 1809.0287 pyterrier.chatnoir_pipelines.retrieve_by_default_text
1 Q0 clueweb09-en0054-92-07350 3 1655.2092 pyterrier.chatnoir_pipelines.retrieve_by_default_text
```

## Submit the Image to TIRA

You need a team for your submission, in the following, I use `tira-ir-starter` as team name, to resubmit the image, please just replace `tira-ir-starter` with your team name.

First, you have to upload the image:

```
docker pull webis/tira-ir-starter-chatnoir:0.0.2
docker tag webis/tira-ir-starter-chatnoir:0.0.2 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/chatnoir:0.0.2
docker push registry.webis.de/code-research/tira/tira-user-tira-ir-starter/chatnoir:0.0.2
```

After the image is uploaded, you should use the following command in TIRA:

``` 
/workspace/retrieve-with-chatnoir.sh --input $inputDataset --output $outputDir
```

Please refer to the general tutorial on [how to import your retrieval approach to TIRA](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters#adding-your-retrieval-software) and on [how to run your retrieval software in TIRA](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters#running-your-retrieval-software) for more detailed instructions on how to submit.



## Building the image:

To build the image and to deploy it in TIRA, please run the follwoing commands:

```
docker build -t webis/tira-ir-starter-chatnoir:0.0.2 -f chatnoir/Dockerfile .
docker push webis/tira-ir-starter-chatnoir:0.0.2
```


