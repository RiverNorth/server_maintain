#!/bin/bash
if [ `ulimit -c` = unlimited ]
then
    if [ `ulimit -n` = 8192 ]
    then
	echo "begin BS04 ..."
	(./BS04 &>bs.log&)
    else
	echo "BS04 start failed! Please run command 'ulimit -n 8192' first"
    fi
else
    echo "BS04 start failed! Please run command 'ulimit -c unlimited' first"
fi
