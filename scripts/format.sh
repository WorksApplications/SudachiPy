#!/usr/bin/env bash

cd $(dirname $0)

flake8 --show --config=flake8.cfg ../sudachipy
flake8 --show --config=flake8.cfg ../tests

HEADER=`cat license-header.txt`

cd ..

array=()

for FILE in `find ./sudachipy -type f -name "*.py"`; do
    array+=( ${FILE} )
done

for FILE in `find ./tests -type f -name "*.py"`; do
    array+=( ${FILE} )
done

array+=( ./setup.py )

for FILE in ${array[@]}; do
    FILECONTENTS=`cat ${FILE}`
    if [[ ${FILECONTENTS} != ${HEADER}* ]]; then
        >&2 echo "invalid license header on ${FILE}"
    fi
done
