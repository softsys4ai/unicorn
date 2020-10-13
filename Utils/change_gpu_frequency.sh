#!/bin/sh
system=$1
new_freq=$2
cur_freq=$3
if [ $system = 'TX1' ]
then 
     filename="/sys/kernel/debug/clock/override.gbus/rate"
     echo $new_freq > $filename

elif [ $system = 'TX2' ]
then
   rail_gate="/sys/devices/17000000.gp10b/railgate_enable"
   max_file="/sys/devices/17000000.gp10b/devfreq/17000000.gp10b/max_freq"
   min_file="/sys/devices/17000000.gp10b/devfreq/17000000.gp10b/min_freq"
   echo 0 > $rail_gate
   if [ $cur_freq -gt $new_freq ]
   then
       echo $new_freq > $min_file
       echo $new_freq > $max_file
   else
       echo $new_freq > $max_file
       echo $new_freq > $min_file
   fi

else
   echo "hardware not supported"
fi
