#!/bin/sh
cpu_name=$1 
operation=$2
filename="/sys/devices/system/cpu/$cpu_name/online"
echo $operation > $filename

