#!/bin/bash
if [ `ulimit -c` = unlimited ]
then
    if [ `ulimit -n` = 8192 ]
    then
	echo "begin DBA04 ..."
	(./DBA04 &>dba.log&)
    else
	echo "DBA04 start failed! Please run command 'ulimit -n 8192' first"
    fi
else
    echo "DBA04 start failed! Please run command 'ulimit -c unlimited' first"
fi
