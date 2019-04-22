#!/bin/sh
system=$1
status=$2
if [ $system = 'TX1' ]
then
    filename="/sys/kernel/debug/clock/override.gbus/state"
elif [ $system = 'TX2' ]
then
    filename="/sys/kernel/debug/bpmp/debug/clk/gpu/state"
else
    echo "hardware not supported"
    exit 1
fi
echo $status > $filename

