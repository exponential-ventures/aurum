#!/usr/bin/env bash

set -e

apt-get install vim -y

pip install sklearn py-spy

tmp_dir=$(mktemp -d)

cd "$tmp_dir"; au init;

cp /usr/src/app/example.py "$tmp_dir"/src


