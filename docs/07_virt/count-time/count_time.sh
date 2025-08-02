#!/usr/bin/env bash
COUNTER=1
while true
do
    echo $COUNTER $(date "+%H:%M:%S")
    COUNTER=$(expr $COUNTER + 1)
    sleep 1
done
