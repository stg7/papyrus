#!/bin/bash
if [ ! -f py/bin/activate ]; then
    echo -e "\033[91m[ERROR] \033[0mfirst start prepare.sh to install python locally"
    exit 1
fi
. py/bin/activate

./papyrus.py "$@"
