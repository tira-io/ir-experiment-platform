# TIRA IR-Starter for ChatNoir

This directory contains a retrieval system that uses the REST API of ChatNoir to retrieve documents from large corpora such as the ClueWeb09, the ClueWeb12, or the ClueWeb22.
ChatNoir is reachable from within TIRA, and we keep the REST API of ChatNoir compatible to ensure reproducibility over the years.

Overall, this starter (or other versions derived from the starter, maybe with custom Query Expansion or similar) can serve as full-rank retriever against huge corpora.
TIRA injects the to-be-used credentials (i.e., the API key and index) in a configuration file, so that an approach can run in multiple shared tasks.

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

The following screenshot shows how the valid configuration in TIRA might look like:



## Building the image:

To build the image and to deploy it in TIRA, please run the follwoing commands:

```
docker build -t webis/tira-ir-starter-chatnoir:0.0.2 -f chatnoir/Dockerfile .
docker push webis/tira-ir-starter-chatnoir:0.0.2
```


