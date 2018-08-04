[ "$TESTSHELL" = "/bin/bash" ] && shopt -s expand_aliases

cp "$TESTDIR"/../*.py .

export PYTHONPATH=$PYTHONPATH:$TESTDIR/../
export LC_ALL=C.UTF-8
