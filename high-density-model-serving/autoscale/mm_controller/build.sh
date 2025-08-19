#!/bin/bash
IMAGE=quandvrobusto/mm-operator:0.0.1
docker build -t $IMAGE .
docker push $IMAGE