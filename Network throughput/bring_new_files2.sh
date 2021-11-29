#!/bin/bash

#######################################################Overwrite old directories#################################################

/usr/bin/rm -rf /home/ahmed/network_throughput/newsite 
/usr/bin/rm -rf /home/ahmed/network_throughput/oldsite
/usr/bin/mkdir /home/ahmed/network_throughput/newsite
/usr/bin/mkdir /home/ahmed/network_throughput/oldsite

#######################################################list last two added files#################################################

cd /home/eniquser/throughput
/usr/bin/ls -t | /usr/bin/head -n 2 > /home/ahmed/network_throughput/new_files.txt
/usr/bin/cd /home/ahmed/network_throughput
x=$(/usr/bin/awk 'NR==1' /home/ahmed/network_throughput/new_files.txt)
y=$(/usr/bin/awk 'NR==2' /home/ahmed/network_throughput/new_files.txt)

#########################################################copy and extract listed files###########################################

/usr/bin/cp -rf /home/eniquser/throughput/$x /home/ahmed/network_throughput/newsite/$x
/usr/bin/unzip -o /home/ahmed/network_throughput/newsite/$x -d /home/ahmed/network_throughput/newsite
/usr/bin/cp -rf /home/eniquser/throughput/$y /home/ahmed/network_throughput/oldsite/$y
/usr/bin/unzip -o /home/ahmed/network_throughput/oldsite/$y -d /home/ahmed/network_throughput/oldsite

