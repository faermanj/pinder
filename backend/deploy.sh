#!/bin/bash

export BUCKET_NAME=pinder-artifacts-artifactsbucket-1l67xiqr2ytsq
export OUT_TEMPLATE=target/template.out.yaml

mkdir -p target

aws cloudformation package \
  --template-file ./template.yaml \
  --s3-bucket $BUCKET_NAME \
  --output-template-file $OUT_TEMPLATE

aws cloudformation deploy \
  --template-file $OUT_TEMPLATE \
  --stack-name pinder-cards-$RANDOM \
  --capabilities CAPABILITY_IAM
  