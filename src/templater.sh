#!/usr/bin/env bash
python -B template_engine.py $1 $2 $3
echo $'The Final Output :'
cat $3
echo $'\n'
