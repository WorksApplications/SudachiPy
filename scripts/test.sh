#!/usr/bin/env bash

# print error message only when it fails
# python unittest print message in stderr even if it succeed
# You need to prepare system.dic in resources and tests/resources
# see README

cd $(dirname $0)
RES=`cd ..; python -m unittest discover tests -p '*test*.py' 2>&1`
RES_TAIL=`echo "$RES" | tail -1`
if [[ $RES_TAIL != "OK" ]]; then
    >&2 echo "$RES"
fi
