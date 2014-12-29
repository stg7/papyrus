#!/bin/bash
#
#    Codestyle checker
#
#    Author: Steve Göring
#

################################################################################
#    log* functions are copied from core/bashhelper
#
#    Printout error to stderr.
#
logError() {
    echo -e "\033[91m[ERROR]\033[0m $@ " 1>&2;
}

#
#    Printout info message.
#
logInfo() {
    echo -e "\033[92m[INFO ]\033[0m $@"
}
################################################################################

checkResult() {
    if [ "$?" == "0" ]; then
        logInfo ".. ok"
    else
        logError ".. fail"
    fi
}

CheckCodeConvetions() {
    # code conventions
    logInfo "check code conventions"
    for i in $(find . -name "*.py" | grep -v "py/" | grep -v "gscholar.py")
    do
        logInfo "check $i "
        # ignore just this stupid 80 char long lines rule
        pep8 --ignore=E501 "$i"
        checkResult
    done
}

CheckCodeConvetions
