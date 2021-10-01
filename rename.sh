#!/usr/bin/env bash

for i in *.tpq; do name=`echo $i | awk -F. '{print $1}'`; mv $i $name.TPQ; done
