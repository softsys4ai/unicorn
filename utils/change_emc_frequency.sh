#!/bin/sh
system=$1
freq=$2

if [ $system = 'TX1' ]
then
    filename="/sys/kernel/debug/clock/override.emc/rate"
elif [ $system = 'TX2' ]
then
    update_file="/sys/kernel/debug/bpmp/debug/clk/emc/rate"
    override_file="/sys/kernel/debug/bpmp/debug/clk/emc/mrq_rate_locked"
    echo $freq > $update_file
    echo 1 > $override_file
    
elif [ $system = 'Xavier' ]
then
    update_file="/sys/kernel/debug/bpmp/debug/clk/emc/rate"
    override_file="/sys/kernel/debug/bpmp/debug/clk/emc/mrq_rate_locked"
    echo $freq > $update_file
    echo 1 > $override_file
    
else
    echo "$system"
    exit 1
fi


