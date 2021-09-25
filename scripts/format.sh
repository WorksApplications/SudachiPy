#!/usr/bin/env bash

cd $(dirname $0)

flake8 --show --config=flake8.cfg ../sudachipy
flake8 --show --config=flake8.cfg ../tests

cd ..
scripts/checkheader.sh