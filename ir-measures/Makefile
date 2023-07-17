IMAGE_VERSION=1.0.6

build-docker-image:
	docker build -t webis/ir_measures_evaluator:dev-${IMAGE_VERSION} -f Dockerfile.dev .
	docker build -t webis/ir_measures_evaluator:${IMAGE_VERSION} .

.PHONY: tests
tests:
	pytest

example-execution:
	rm -Rf output
	docker run --rm -it -v ${PWD}/input:/input -v ${PWD}/output:/output webis/ir_measures_evaluator:${IMAGE_VERSION} --run /input/run.txt --qrels /input/qrels.txt --measures "AP(rel=2)" "P(rel=2)@10" --output_path /output/eval.prototext

publish-docker-image:
	docker push webis/ir_measures_evaluator:${IMAGE_VERSION}
