#!/bin/bash -x

DATE_DIR_NAME=$(date + "%W%y")
mkdir -p /container_output/$DATE_DIR_NAME

if [ -z "$@" ]
then
    python3 -m run
else
    python3 -m run "$@"
fi

mv /app/output/* /container_output/$DATE_DIR_NAMEsource
