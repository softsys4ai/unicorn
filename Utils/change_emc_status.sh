#!/bin/sh
system=$1
status=$2
filename="/sys/kernel/debug/clock/override.emc/state
if [ $system = 'TX1' ]
then
    filename="/sys/kernel/debug/clock/override.emc/state"
elif [ $system = 'TX2' ]
then
    filename="/sys/kernel/debug/bpmp/debug/clk/emc/state"
else
    echo "hardware not supported"
    exit 1 
fi


echo $status > $filename

