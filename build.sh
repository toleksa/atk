#!/usr/bin/env bash
#
# ./build.sh [tag] [name]
#

PWD=$(pwd)
PROJECT=$(dirname "$(readlink -f "$0")" | gawk -F"/" '{ print $NF }')

CMD="docker build -t ${2:-$PROJECT}:${1:-latest} ."
echo $CMD
eval $CMD

