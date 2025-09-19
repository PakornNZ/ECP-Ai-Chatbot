#!/bin/sh
ollama serve &
pid=$!
sleep 5

ollama create ${RESPONSE_MODEL} -f ./finetune/Modelfile.txt

wait $pid