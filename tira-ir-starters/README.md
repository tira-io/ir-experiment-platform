# TIRA IR Starters

We provide starters for 4 frequently used IR research frameworks that can be used as basis for software submissions to the Information Retrieval Experiment Platform. The simplest starter implements BM25 retrieval using a few lines of declarative PyTerrier code in a Jupyter notebook.

Retrieval Systems submitted to the IR Experiment Platform have to be implemented in fully self-contained Docker images, i.e., the software must be able to run without internet connection to improve reproducibility (e.g., preventing cases where an external dependency or API is not available anymore in a few years).

Our existing starters can be directly submitted to TIRA, as all of them have been extensively tested on 32 benchmarks in TIRA, and they also might serve as starting point for custom development.

## Local Development

Please use the `tira-run` command (can be installed via `pip3 install tira`) to test that your retrieval approach is correctly installed inside the Docker image.
Each tira-ir-starter comes with a dedicated `tira-run` example that shows how you can test your docker image locally.

## Available Starters

The following starters are available:

- [Dense Retrieval starters from BEIR](beir): 17 starters for modern bi-encoder approaches.
- [ChatNoir](chatnoir): BM25F retrieval via an REST API from huge corpora, such as the ClueWeb09, the ClueWeb12, or the ClueWeb22.
- [PyGaggle](pygaggle): 8 starters for cross-encoder models such as monoBERT or monoT5.
- [PyTerrier](pyterrier): 20 starters for lexical models such as BM25 or PL2.
- [DuoT5@PyTerrier](pyterrier-duot5): 3 starters using the DuoT5 approach implemented in the PyTerrier Plugin for DuoT5.
- [ColBERT@PyTerrier](pyterrier-colbert): Implementation of ColBERT in the PyTerrier Plugin.


## Adding your Retrieval Software

To import your retrieval approach to TIRA, please first upload your image (you can use one of the [available starters](#available-starters) using your dedicated credentials. You can find a personalized tutorial on how to upload your image after you have clicked on "Docker Submission" -> "Upload Images":

![personalized-credentials](https://user-images.githubusercontent.com/10050886/221603400-4b0381f0-e743-4876-a455-e45792512e34.png)

For instance, if you have an image `registry.webis.de/code-research/tira/tira-user-<YOUR-TEAM-NAME>/my-software:0.0.1`, you can upload it as described in your personalized tutorial via:

```
docker login -u tira-user-<YOUR-TEAM-NAME> -p<PASSWORD-REMOVED> registry.webis.de
docker push registry.webis.de/code-research/tira/tira-user-<YOUR-TEAM-NAME>/my-software:0.0.1
```

After you have uploaded your image, you can add a new Software by clicking on "Docker Submission" -> "Add Container":

![tira-define-job](https://user-images.githubusercontent.com/10050886/221604262-715013c3-843f-4393-9894-e842c4718f7d.png)

## Running your Retrieval Software

After you have added the new software, you can run it on suitable datasets.

![software-already-configured](https://user-images.githubusercontent.com/10050886/221604580-3dffecd3-f774-44c7-9103-690f4c04a9b3.png)




