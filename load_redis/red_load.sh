#!/bin/sh

./merge.sh
./load.rb | redis-cli --pipe
