#!/bin/sh

python gao.py > out_se
node gao.js > out_ts
paste -d" " out_ts out_se > out
