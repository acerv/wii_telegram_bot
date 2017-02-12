#!/bin/sh
# Update the Synology NAS.

if [ -z $1 ] | [ -z $2 ] | [ -z $3 ]; then
    echo ""
    echo "Usage: $0 <user> <ip> <port>"
    echo ""
    exit 1
fi

user=$1
ip=$2
port=$3

ssh $user@$ip -p $port \
    "
    cd /volume1/@appstore/wii_telegram_bot ;
    git pull origin master ;
    sudo -S S99wii_telegram_bot.sh /usr/syno/etc.defaults/rc.sysv/S99wii_telegram_bot.sh ;
    sudo -S /usr/syno/etc.defaults/rc.sysv/S99wii_telegram_bot.sh stop ;
    sudo -S /usr/syno/etc.defaults/rc.sysv/S99wii_telegram_bot.sh start
    "
