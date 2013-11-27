#!/bin/bash

ps afx | grep "main.js"  | while read line
do
        if [[ $line == *grep* || $line == *$0* ]];
        then
                continue
        fi
        arr=($line)
        nodepid=${arr[0]}
        taskset -p 1 $nodepid
done

ps afx | grep redis  | while read line
do
        if [[ $line == *grep* || $line == *$0* ]];
        then
                continue
        fi
        arr=($line)
        redispid=${arr[0]}
        taskset -p 2 $redispid
done
