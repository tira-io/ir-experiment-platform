
Add the evaluator to tira with:

Image:
```
webis/ir_measures_evaluator:1.0
```

Command (if no qrels are available):

```
/ir_measures_evaluator.py --run ${inputRun}/run.txt --output_path ${outputDir}/evaluation.prototext
```


Command (if qrels are available):

```
/ir_measures_evaluator.py --run ${inputRun}/run.txt --topics ${inputDataset}/queries.jsonl --qrels ${inputDataset}/qrels.txt --output_path ${outputDir} --measures "P@10" "nDCG@10" "MRR"
```

