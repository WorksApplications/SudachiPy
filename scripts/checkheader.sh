#!/usr/bin/env bash

HEADER=scripts/license-header.txt
SIZE=`wc -c < "$HEADER"`

RES=`find setup.py sudachipy tests -type f -name '*.py' -exec cmp -n "$SIZE" "$HEADER" {} \;`
if [ -n "$RES" ]; then
    echo "$RES" | awk '{print "invalid license header on " $2}' >&2
    exit 1
fi