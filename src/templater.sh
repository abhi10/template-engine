#!/usr/bin/env bash
#the following arguments can also be read from command line
a="template.panoramatemplate"
b="data.json"
c="output.html"
python -B template_engine.py "$a" "$b" "$c"
echo $'The Final Output :'
cat $c
echo $'\n'
