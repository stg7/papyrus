#!/usr/bin/env python3
"""
    Papyrus

    unify and sort scientiftic pdf papers

    author: Steve Göring
    contact: stg7@gmx.de
    2014
"""
"""
    This file is part of Papyrus.

    Papyrus is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Papyrus is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Papyrus.  If not, see <http://www.gnu.org/licenses/>.
"""
import argparse
import sys
import os
import io
import shelve
import logging
import time
import random
import shutil

import loader

from log import *
from lib import *

import gscholar
import bibtexparser

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.pdfdevice import TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams


def extract_from_pdf(file_name):
    # disable logging, because pdfminer produces a lot of warnings
    logger = logging.getLogger()
    logger.disabled = True

    f = open(file_name, "rb")
    laparams = LAParams()

    try:
        rsrcmgr = PDFResourceManager(caching=True)
        out = io.StringIO()
        device = TextConverter(rsrcmgr, out, laparams=laparams)
        process_pdf(rsrcmgr, device, f, set(), maxpages=1, check_extractable=True)
        s = unligaturify(str(out.getvalue()))
        out.close()

        tt = " ".join(s.replace("\n", " ").replace("  ", " ").split(" "))

        """ extract title """
        tmp = s.split("\n")[0:5]
        idx = tmp.index("")
        title = " ".join(tmp[0:idx])
        f.close()

        meta = {"title": title.strip(), "keywords": extract_key_words(tt)}
        return meta

    except Exception as e:
        lError(e)
        return {"title": "", "keywords": []}


def short_year(year):
    return year[-2:]


def customizations(record):
    record = bibtexparser.customization.type(record)
    record["id"] = record["author"].split(",", 1)[0].lower() + short_year(record.get("year", "aaaa"))
    record["id"] = record["id"].replace("{", "").replace("}", "").replace("\\", "").replace("'", "")
    return record


def scholar_get(title, db):
    print(gscholar.query("linked open data", allresults=True))

    if title not in db:
        query = gscholar.query(title)
        if len(query) < 1:
            return {"title": "", "authors": [], "year": "", "bibtex": ""}
        db[title] = query[0]
        time.sleep(random.randint(0, 10))

    meta = {}

    parser = bibtexparser.bparser.BibTexParser()
    parser.customization = customizations
    raw_entry = bibtexparser.loads(db[title], parser=parser)
    entry = raw_entry.entries[0]

    meta["title"] = entry['title'].strip()
    meta["authors"] = entry['author'].replace(", ", " ").split("and")
    meta["year"] = entry.get('year', "").strip()
    meta["bibtex"] = bibtexparser.dumps(raw_entry)

    return meta


def convert_filename(i):
    disallowed_chars = "!,#+?=)(/&%$§ "

    i = i.replace("{", "").replace("}", "").replace("\\", "").replace("'", "")

    converted_filename = i.lower()
    for d in disallowed_chars:
        converted_filename = converted_filename.replace(d, "-")
    return converted_filename + ".pdf"


def process_file(file_name, outputdir, db):
    pdf_infos = extract_from_pdf(file_name)
    title_text = pdf_infos["title"]
    scholar_infos = scholar_get(title_text, db)
    title_scholar = scholar_infos["title"]

    if len(scholar_infos["authors"]) == 0:
        lError("something wrong with: " + file_name)
        return ""

    sim = string_sim(title_text, title_scholar)

    lInfo("process file: " + file_name)
    lDbg("keywords: " + str(pdf_infos["keywords"]))
    lDbg("title_text: " + title_text)
    lDbg("title_scholar: " + title_scholar)
    lDbg("sim: " + str(sim))

    bib_entry = scholar_infos["bibtex"]

    if sim > 0.9:
        name = " ".join([scholar_infos["authors"][0].split(" ")[0] + short_year(scholar_infos["year"]), scholar_infos["title"]])
        new_file_name = outputdir + "/" + convert_filename(name)
        if os.path.isfile(new_file_name):
            lWarn("detect duplicated pdf: " + new_file_name)
        else:
            lInfo("ok- move & rename file: " + os.path.basename(new_file_name))
            shutil.move(file_name, new_file_name)
            return bib_entry
    else:
        lError("problem with: " + file_name + ", rename manually")
    return ""


def read_bib_keys(file_name):
    if not os.path.isfile(file_name):
        return set()
    f = open(file_name, "r")
    keys = set()
    for l in f:
        if re.match("@.*{", l):
            key = re.sub("@.*{", "", l.strip()).replace(",", "")
            keys.add(key)
    f.close()

    return keys


def main(args):

    # argument parsing
    parser = argparse.ArgumentParser(description='Papyrus - unify scientiftic pdf papers', epilog="stg7 2014")
    parser.add_argument('pdf_file', type=str, nargs='+', help='pdf file to process')
    parser.add_argument('-o', dest='outputdir', type=str, default="out", help='output directory, default: out')

    argsdict = vars(parser.parse_args())
    outputdir = os.getcwd() + "/" + argsdict['outputdir']
    create_dir_if_not_exists(outputdir)

    file_list = argsdict["pdf_file"]

    db = shelve.open("cache")

    stored_bib_entrie_keys = read_bib_keys(outputdir + "/lit.bib")

    bib_entries = []

    for file_name in filter(lambda x: ".pdf" in x, file_list):
        bib_entries.append(process_file(file_name, outputdir, db))

    # build lit.bib file

    bib_file = open(outputdir + "/lit.bib", "a")
    for b in bib_entries:
        key = re.sub("@.*{", "", b.split("\n", 1)[0].strip()).replace(",", "")
        new_key = key
        if key in stored_bib_entrie_keys:
            i = 0
            for k in stored_bib_entrie_keys:
                if key in k:
                    i += 1
            new_key += chr(ord("a") + i - 1)

        b = b.replace("{" + key + ",", "{" + new_key + ",")
        stored_bib_entrie_keys.add(new_key)
        bib_file.write(b + "\n")

    bib_file.close()

    db.close()


if __name__ == "__main__":
    main(sys.argv[1:])
