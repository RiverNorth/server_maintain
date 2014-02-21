#!/bin/bash
if [ `ulimit -c` = unlimited ]
then
    if [ `ulimit -n` = 8192 ]
    then
	echo "begin LS04 ..."
	(./LS04 &>ls.log&)
    else
	echo "LS04 start failed! Please run command 'ulimit -n 8192' first"
    fi
else
    echo "LS04 start failed! Please run command 'ulimit -c unlimited' first"
fi
