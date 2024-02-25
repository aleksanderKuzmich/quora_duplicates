#!/bin/bash

WORK_DIR="/home/alex/Documents/studia/sem_VIII/AJiO/testing"

docker run \
    --rm \
    --name quora-runner \
    -v "${WORK_DIR}/.env:/app/src/.env" \
    -v "${WORK_DIR}/train.csv:/app/input/train.csv" \
    -v "${WORK_DIR}/container_output:/container_output" \
    "quora-duplicates"
