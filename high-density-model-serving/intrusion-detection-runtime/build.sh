#!/bin/bash
IMAGE_NAME=quandvrobusto/intrusion-detection-mm:0.0.20
docker build -t $IMAGE_NAME .
docker push $IMAGE_NAME