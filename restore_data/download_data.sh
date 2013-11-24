#!/bin/bash
mkdir /mnt/tb2
mkdir /mnt/tb3
mkdir /mnt/tb4

s3cmd get s3://proj_hbase_backup/export_tb2/* /mnt/tb2/ &
s3cmd get s3://proj_hbase_backup/export_tb3/* /mnt/tb3/ &
s3cmd get s3://proj_hbase_backup/export_tb4/* /mnt/tb4/ &

