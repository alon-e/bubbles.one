#!/bin/sh

user_name=$1
SSID=$(cat $user_name.ssid)
# Configure Wi-Fi
uci delete wireless.$user_name
uci set wireless.$user_name=wifi-iface
uci set wireless.$user_name.device=radio0
uci set wireless.$user_name.mode=ap
uci set wireless.$user_name.network=lan
uci set wireless.$user_name.ssid=$SSID
uci set wireless.$user_name.encryption=none
