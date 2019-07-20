#!/usr/bin/env bash

cd $(dirname $0)

HEADER=`cat license-header.txt`

cd ..

for FILE in `find ./sudachipy -type f -name "*.py"`
do
    FILECONTENTS=`cat ${FILE}`
    if [[ ${FILECONTENTS} != ${HEADER}* ]]; then
        echo ${HEADER} | echo - ${FILECONTENTS} > tmp && mv tmp ${FILE}
    fi
done

for FILE in `find ./tests -type f -name "*.py"`
do
    FILECONTENTS=`cat ${FILE}`
    if [[ ${FILECONTENTS} != ${HEADER}* ]]; then
        echo ${FILE}
    fi
done

FILECONTENTS=`cat setup.py`
if [[ ${FILECONTENTS} != ${HEADER}* ]]; then
    echo ${FILE}
fi
