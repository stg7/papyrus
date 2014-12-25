#!/bin/bash
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

echo -e "\033[92m done. \033[0m"



