#!/bin/bash

INTERVAL=30


while :
do
  echo "Updating Network list..."
  
  for file in *.seed
    do
    # run python script to update tokens
    user_name=$(echo $file | sed 's/.seed//')
    user_name=(${user_name//$'\n'/ })
    echo $user_name
    #echo $user_name
    python ./run_ssid.py $user_name
    
    #update network
    ./update_network.sh $user_name
    echo $data
  done
  
  uci commit
  /etc/init.d/network restart
  
  sleep $INTERVAL
done