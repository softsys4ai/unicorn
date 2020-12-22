#!/bin/sh
system=$1
new_freq=$2
cur_freq=$3

min_file="/sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq"
max_file="/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq"
governor_file="/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
echo userspace > $governor_file
if [ $system = 'TX2' ]
then
    echo 0 > /sys/module/qos/parameters/enable
    echo 0 > /sys/kernel/debug/tegra_cpufreq/M_CLUSTER/cc3/enable
    echo 0 > /sys/kernel/debug/tegra_cpufreq/B_CLUSTER/cc3/enable
fi

if [ $cur_freq -gt $new_freq ]
then
    echo $new_freq > $min_file
    echo $new_freq > $max_file
else
    echo $new_freq > $max_file
    echo $new_freq > $min_file
fi
