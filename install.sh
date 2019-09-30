#!/usr/bin/env bash

export PIP_CONFIG_FILE=~/.pip.conf

rm -Rf .conda
rm -Rf .ipynb_checkpoints

conda env create -f environment.yml -p .conda
