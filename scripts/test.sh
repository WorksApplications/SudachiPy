#!/usr/bin/env bash

# print error message only when it fails
# python unittest print message in stderr even if it succeed
# You need to prepare system.dic in resources and tests/resources
# see README

cd $(dirname $0)

# check system.dic
if [[ ! -f "../tests/resources/system.dic" ]]; then
    cp ../.travis/system.dic.test ../tests/resources/system.dic
fi
DIFF=$(diff ../.travis/system.dic.test ../tests/resources/system.dic)
if [[ "$DIFF" != "" ]]; then
    cp ../.travis/system.dic.test ../tests/resources/system.dic
fi

# check user.dic
if [[ ! -f "../tests/resources/user.dic" ]]; then
    cp ../.travis/user.dic.test ../tests/resources/user.dic
fi
DIFF=$(diff ../.travis/user.dic.test ../tests/resources/user.dic)
if [[ "$DIFF" != "" ]]; then
    cp ../.travis/user.dic.test ../tests/resources/user.dic
fi

# unittest
RES=`cd ..; python3.7 -m unittest discover tests -p '*test*.py' 2>&1`
RES_TAIL=`echo "$RES" | tail -1`
if [[ $RES_TAIL != "OK" ]]; then
    >&2 echo "$RES"
fi
