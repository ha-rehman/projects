#!/bin/bash

cd /tmp

if [ -d pypi ]; then
    rm -Rf pypi
fi

mkdir pypi

cd pypi

python3 -m venv programy

cd programy

source ./bin/activate

pip3 install --no-cache-dir programy

python3 -m programy.admin.tool

python3 -m programy.admin.tool install textblob

python3 -m programy.admin.tool download y-bot

python3 -m programy.clients.embed.basic

deactivate

cd /tmp

rm -Rf pypi
