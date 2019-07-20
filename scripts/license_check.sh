#!/usr/bin/env bash

cd $(dirname $0)

HEADER=`cat license-header.txt`

cd ..

for FILE in `find ./sudachipy -type f -name "*.py"`
do
    FILECONTENTS=`cat ${FILE}`
    if [[ ${FILECONTENTS} != ${HEADER}* ]]; then
        >&2 echo "no license header on ${FILE}"
    fi
done

for FILE in `find ./tests -type f -name "*.py"`
do
    FILECONTENTS=`cat ${FILE}`
    if [[ ${FILECONTENTS} != ${HEADER}* ]]; then
        >&2 echo "no license header on ${FILE}"
    fi
done

FILECONTENTS=`cat setup.py`
if [[ ${FILECONTENTS} != ${HEADER}* ]]; then
    >&2 echo "no license header on setup.py"
fi
