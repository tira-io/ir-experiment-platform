# IR Measures Evaluator

The IR Measures evaluator uses the truth data (e.g., qrels) and the outputs of a system (e.g., a run) as input to produce an evaluation. This evaluator produces both, a quantitative evaluation with ir_measures (e.g., P@10, nDCG@10) but also the basis for qualitative evaluations by rendering the runs into search engine result pages. Both, the rendered SERP and the effectiveness measures are stored in the evaluation directory so that participants can see both if a run and evaluation is unblinded.

To test the evaluator locally, please install `tira-run` (e.g., `pip3 install tira`) which executes an docker image as it would be executed in TIRA and use the following command from within this directory to try it on your local system on a small example:

```
tira-run \
	--image webis/ir_measures_evaluator:1.0.3 \
	--input-run ${PWD}/tests/end-to-end-test/output-of-run/ \
	--input-directory ${PWD}/tests/end-to-end-test/truth-data/ \
	--output-directory ${PWD}/tests/end-to-end-test/evaluator-output \
	--allow-network true \
	--command '/ir_measures_evaluator.py --run ${inputRun}/run.txt --topics ${inputDataset}/queries.jsonl --qrels ${inputDataset}/qrels.txt --output ${outputDir} --measures "P@10" "nDCG@10" "MRR"'
```

This creates a directory `tests/end-to-end-test/evaluator-output/` with the following content:

- `evaluation-per-query.prototext`: Per query evaluations (e.g., for significance tests)
- `evaluation.prototext`: Evaluations
- `serp.html`: The rendered SERP for all topics
- `.data-top-10-for-rendering.jsonl`: Small export of all the data required for rendering the run. This is intended for more dynamic rendering.

# Usage in TIRA

Add the evaluator to tira with:

Image:
```
webis/ir_measures_evaluator:1.0.2
```

Command (if no qrels are available):

```
/ir_measures_evaluator.py --run ${inputRun}/run.txt --output_path ${outputDir}/evaluation.prototext
```


Command (if qrels are available):

```
/ir_measures_evaluator.py --run ${inputRun}/run.txt --topics ${inputDataset}/queries.jsonl --qrels ${inputDataset}/qrels.txt --output_path ${outputDir} --measures "P@10" "nDCG@10" "MRR"
```

