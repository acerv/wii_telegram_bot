#!/bin/sh
# Boot script for Synology SysV
# Author: Andrea Cervesato <andrea.cervesato@mailbox.org>

PYTHON_EXEC="/usr/bin/python2.7"
SCRIPT_EXEC="/volume1/@appstore/wii_telegram_bot/src/wiibot.py"

case $1 in
start)
	PATH=$PATH:/volume1/@appstore/python/bin
	printf "%-30s" "Starting script"
	${PYTHON_EXEC} ${SCRIPT_EXEC} &
	printf "[%4s]\n" "done"
	;;
stop)
	printf "%-30s" "Stopping script"
	pkill -f ${SCRIPT_EXEC}
	printf "[%4s]\n" "done"
	;;
*)
	echo "Usage: $0 {start|stop}"
	exit 1
	;;
esac

exit 0
