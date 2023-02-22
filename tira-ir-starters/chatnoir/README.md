
docker build -t webis/tira-ir-starter-chatnoir:0.0.1 -f chatnoir/Dockerfile .
docker tag webis/tira-ir-starter-chatnoir:0.0.1 registry.webis.de/code-research/tira/tira-user-tira-ir-starter/chatnoir:0.0.1

docker push registry.webis.de/code-research/tira/tira-user-tira-ir-starter/chatnoir:0.0.1
 
/workspace/retrieve-with-chatnoir.sh --input $inputDataset --output $outputDir
