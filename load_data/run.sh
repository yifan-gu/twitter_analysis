#!/bin/bash
java -cp ".:hbase-0.94.13.jar:hadoop-core-1.2.1.jar:lib/*:gson-2.2.4.jar" loadData $1 > load.log 2> load.log

# $1 is config file
