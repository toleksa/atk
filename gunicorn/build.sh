#!/usr/bin/env bash
if [ $# -eq 0 ]
  then
    TAG='latest'
  else
    TAG=$1
fi

PWD=$(pwd)
PROJECT=$(dirname "$(readlink -f "$0")" | gawk -F"/" '{ print $NF }')

docker build -t $PROJECT:$TAG .

