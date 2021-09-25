#!/usr/bin/env bash

# print error message only when it fails
# python unittest print message in stderr even if it succeed
# You need to prepare system.dic in resources and tests/resources
# see README

set -e

# build dictionaries
python -m sudachipy.command_line build -o tests/resources/system.dic -d "the system dictionary for the unit tests" -m tests/resources/dict/matrix.def tests/resources/dict/lex.csv
python -m sudachipy.command_line ubuild -o tests/resources/user.dic -s tests/resources/system.dic tests/resources/dict/user.csv

set +e

# unittest
RES=`python -m unittest discover tests -p '*test*.py' 2>&1`
STATUS=$?
RES_TAIL=`echo "$RES" | tail -1`
if [[ $RES_TAIL != "OK" ]]; then
    >&2 echo "$RES"
fi

exit $STATUS