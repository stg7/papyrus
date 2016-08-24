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
pip3 install --upgrade pip

pip3 install pylev
pip3 install numpy
pip3 install nltk
pip3 install bibtexparser
pip3 install pdfminer3k

cd py
git clone https://github.com/venthur/gscholar.git
cd ..
cp py/gscholar/gscholar/gscholar.py libs/

logInfo "done."



