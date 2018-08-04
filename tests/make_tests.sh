#!/bin/bash

echo "  $ . \"\$TESTDIR\"/setup.sh" 

while read p; do
    echo "  $ python solve.py '$p'"
done

