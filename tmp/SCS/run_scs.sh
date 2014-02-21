#!/bin/bash
if [ `ulimit -c` = unlimited ]
then
    if [ `ulimit -n` = 8192 ]
    then
	echo "begin SCS04 ..."
	(./SCS04 &>scs.log&)
    else
	echo "SCS04 start failed! Please run command 'ulimit -n 8192' first"
    fi
else
    echo "SCS04 start failed! Please run command 'ulimit -c unlimited' first"
fi

