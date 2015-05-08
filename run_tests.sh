#!/bin/sh

if [ ! -d "py3env" ]; then
    virtualenv -p python3.4 py3env
fi

if [ ! -d "py2env" ]; then
    virtualenv -p python2.7 py2env
fi

if [ ! -d "pypyenv" ]; then
    virtualenv -p pypy pypyenv
fi

py2env/bin/python -m test.test_join
py3env/bin/python -m test.test_join
pypyenv/bin/python -m test.test_join
