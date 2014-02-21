#!/bin/bash
if [ `ulimit -c` = unlimited ]
then
    if [ `ulimit -n` = 8192 ]
    then
	echo "begin GS04 ..."
	(./GS04 &>gs.log&)
    else
	echo "GS04 start failed! Please run command 'ulimit -n 8192' first"
    fi
else
    echo "GS04 start failed! Please run command 'ulimit -c unlimited' first"
fi
