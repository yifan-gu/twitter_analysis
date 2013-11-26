#!/bin/sh

./load.rb $(ls out*) | redis-cli --pipe
