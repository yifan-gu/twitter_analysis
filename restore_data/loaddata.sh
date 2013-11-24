#!/bin/bash

echo "put data"
hadoop fs -put /mnt/tb2 /
hadoop fs -put /mnt/tb3 /
hadoop fs -put /mnt/tb4 /

echo "done"

echo "create tables"
hbase org.apache.hadoop.hbase.util.RegionSplitter tb2 -c 200 -f ut
hbase org.apache.hadoop.hbase.util.RegionSplitter tb3 -c 200 -f tw
hbase org.apache.hadoop.hbase.util.RegionSplitter tb4 -c 200 -f usr

echo "done"

echo "import data"

hbase org.apache.hadoop.hbase.mapreduce.Import tb2 /tb2 
hbase org.apache.hadoop.hbase.mapreduce.Import tb3 /tb3 
hbase org.apache.hadoop.hbase.mapreduce.Import tb4 /tb4 

echo "done starting jobs"


