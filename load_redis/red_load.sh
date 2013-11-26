#!/bin/sh

./load.rb | redis-cli --pipe
