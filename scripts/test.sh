#!/usr/bin/env bash

# print error message only when it fails
# python unittest print message in stderr even if it succeed

cd $(dirname $0)
RES=`cd ..; python -m unittest discover tests 2>&1`
RES_TAIL=`echo "$RES" | tail -1`
if [[ $RES_TAIL != "OK" ]]; then
    echo "$RES"
fi
