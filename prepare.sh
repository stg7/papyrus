#!/bin/bash
logError() {
    echo -e "\033[91m[ERROR]\033[0m $@ " 1>&2;
}

logInfo() {
    echo -e "\033[92m[INFO ]\033[0m $@"
}

logDebug() {
    echo -e "\033[94m[DEBUG]\033[0m $@" 1>&2;
}

check_tools() {
    for tool in $@; do
        which $tool > /dev/null

        if [[ "$?" -ne 0 ]]; then
            logError "$tool is not installed."
            exit 1
        fi
    done
    logDebug "Each needed tool ($@) is installed."
}

if [ -d "py" ]; then
    logError "'py' directory already there, exit"
    exit 1
fi

check_tools "python3 pyvenv git"

pyvenv --copies py
. py/bin/activate

pip install pylev
pip install numpy
pip install nltk
pip install bibtexparser
pip install pdfminer3k

cd py
git clone git@github.com:venthur/gscholar.git
cd ..
cp py/gscholar/gscholar/gscholar.py libs/

logInfo "done."



