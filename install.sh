#! /bin/bash

for d in `ls -la | grep ^d | awk '{print $NF}' | egrep -v '^\.'`; do

  ./.src/findbugs.py $(pwd)/$d/bin/pom.xml

  ./readme.sh $d

  ./folder.sh $d

done
