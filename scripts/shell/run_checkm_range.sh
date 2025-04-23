#!/bin/bash

# Check that exactly two arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <start> <end>"
    exit 1
fi

start=$1
end=$2

# Loop from start to end (inclusive)
for (( i=start; i<=end; i++ )); do
    ./run_checkm.sh "$i"
done