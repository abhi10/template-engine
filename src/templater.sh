#!/usr/bin/env bash
#the following arguments can also be read from command line
a="template.sample"
b="data.json"
c="render.html"
python -B template_engine.py "$a" "$b" "$c"
echo $'The Final Output :'
cat $c
echo $'\n'
