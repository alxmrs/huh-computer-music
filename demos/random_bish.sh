#!/usr/bin/env bash

python src/bish.py per ts noise qf -d whole sm vco mul -c 0.05 speaker &
python src/bish.py per ts noise qf -d half sm vco mul -c 0.05 speaker &
python src/bish.py per ts noise qf -d eighth sm vco mul -c 0.05 speaker &
