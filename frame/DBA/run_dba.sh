#!/bin/bash
if [ `ulimit -c` = unlimited ]
then
    if [ `ulimit -n` = 8192 ]
    then
	echo "begin %s ..."
	(./%s &>dba.log&)
    else
	echo "%s start failed! Please run command 'ulimit -n 8192' first"
    fi
else
    echo "%s start failed! Please run command 'ulimit -c unlimited' first"
fi
