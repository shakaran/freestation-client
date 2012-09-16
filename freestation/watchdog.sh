#!/bin/bash

NAME=freestation
START="freestation/watchdog.py"
NOP=/bin/true

ps -ef | grep -v grep | grep $NAME >/dev/null 2>&1
case "$?" in
   0)
	   # It is running in this case so we do nothing.
	   $NOP
   ;;
   1)
	   echo "$NAME is NOT RUNNING. Starting $NAME and sending notices."
	   $START
   ;;
esac

exit