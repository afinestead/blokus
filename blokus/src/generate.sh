#!/bin/bash

rm -rf ./api
openapi-generator-cli generate \
    -i http://localhost:8888/openapi.json \
    -g javascript \
    -o ./api \
    --additional-properties=emitJSDoc=false,projectName=blokusApi,usePromises=true
