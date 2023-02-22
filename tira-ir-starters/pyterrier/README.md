# Indexing Command for TIRA:

docker build -t webis/tira-ir-starter-pyterrier:0.0.1-base -f pyterrier/Dockerfile.base .
docker tag webis/tira-ir-starter-pyterrier:0.0.1-base registry.webis.de/code-research/tira/tira-user-tira-ir-starter/pyterrier:0.0.1

`/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $outputDir`


/workspace/pyterrier_cli.py --input /foo/cranfield --output /tmp --index_directory /tmp/index

/workspace/pyterrier_cli.py --input /foo/cranfield --output /tmp/o --params wmodel=BM25 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve --index_directory /tmp/index

/workspace/pyterrier_cli.py --input /foo/cranfield --output /tmp/o --params wmodel=BM25 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve_rm3 --index_directory /tmp/index

# Retrieval Commands for TIRA:

- BM25: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=BM25 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- BM25+RM3: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=BM25 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve_rm3`
- BB2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=BB2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DFIC: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DFIC --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DFIZ: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DFIZ --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DFR_BM25: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DFR_BM25 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DFRee: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DFRee --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DFReeKLIM: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DFReeKLIM --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`

- DFRWeightingModel: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DFRWeightingModel --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DirichletLM: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DirichletLM --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DLH: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DLH --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- DPH: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=DPH --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- Hiemstra_LM: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=Hiemstra_LM --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`

- IFB2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=IFB2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- In_expB2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=In_expB2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- In_expC2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=In_expC2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- InB2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=InB2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- InL2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=InL2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`

- Js_KLs: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=Js_KLs --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- LGD: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=LGD --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- PL2: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=PL2 --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- TF_IDF: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=TF_IDF --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`
- XSqrA_M: `/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $inputRun --params wmodel=XSqrA_M --retrieval_pipeline default_pipelines.wmodel_batch_retrieve`


# Rerank Commands for TIRA:

docker run --rm -ti -v ${PWD}/tmp-out:/output -v ${PWD}/clueweb-rerank:/input:ro --entrypoint /workspace/pyterrier_cli.py webis/tira-ir-starter-pyterrier:0.0.1-base --input /input --output /output --params wmodel=BM25 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer

docker run --rm -ti -v ${PWD}/tmp-out:/output -v ${PWD}/cranfield-rank:/input:ro --entrypoint /workspace/pyterrier_cli.py webis/tira-ir-starter-pyterrier:0.0.1-base --input /input --output /output --params wmodel=BM25 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer

docker run --rm -ti -v ${PWD}/tmp-out:/output -v ${PWD}/antique-rank:/input:ro --entrypoint /workspace/pyterrier_cli.py webis/tira-ir-starter-pyterrier:0.0.1-base --input /input --output /output --params wmodel=BM25 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer


- BM25 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=BM25 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DFIC Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DFIC --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DFIZ Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DFIZ --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DFR_BM25 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DFR_BM25 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DFRee Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DFRee --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DFReeKLIM Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DFReeKLIM --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DirichletLM Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DirichletLM --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DLH Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DLH --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- DPH Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=DPH --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- Hiemstra_LM Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=Hiemstra_LM --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- IFB2 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=IFB2 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- In_expB2 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=In_expB2 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- In_expC2 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=In_expC2 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- InB2 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=InB2 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- InL2 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=InL2 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- Js_KLs Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=Js_KLs --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- LGD Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=LGD --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- PL2 Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=PL2 --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- TF_IDF Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=TF_IDF --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`
- XSqrA_M Re-Rank (tira-ir-starter-pyterrier): `/workspace/pyterrier_cli.py --input /input --output /output --params wmodel=XSqrA_M --rerank True --retrieval_pipeline default_pipelines.wmodel_text_scorer`












