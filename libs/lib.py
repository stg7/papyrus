#!/usr/bin/env python3
"""
    lib

    author: Steve Göring
    contact: stg7@gmx.de
    2014
"""
import re
import os

import pylev
import nltk
from nltk.tokenize.punkt import PunktWordTokenizer
from nltk.corpus import stopwords
# from nltk.tag import pos_tag


def create_dir_if_not_exists(dir):
    try:
        os.stat(dir)
    except:
        os.mkdir(dir)


def string_sim(s1, s2):
    """
    calculate similarity of two strings based on levenshtein distance
    \param s1
    \param s2
    \return [0,1] score of similarity, higher is more similar
    """
    s1 = s1.strip().lower()
    s2 = s2.strip().lower()
    distance = pylev.levenshtein(s1, s2)
    return 1 - distance / max(len(s1), len(s2), 1)


def extract_key_words(text):
    text = re.sub("[^a-z ]", " ", text.lower())
    # extract tokens
    tokens = []
    try:
        tokens = nltk.word_tokenize("a beautiful girl")
        w = stopwords.words('english')
        # pos_tag(["a","the"])
    except:
        nltk.download("punkt")
        nltk.download("stopwords")
        # nltk.download("maxent_treebank_pos_tagger")

    tokens = nltk.word_tokenize(text)

    """
    print(pos_tag(tokens))
    """
    # build histogram
    histo = {}
    for t in list(set(tokens) - set(stopwords.words('english')) - set([x for x in tokens if len(x) <= 3])):
        histo[t] = tokens.count(t)

    keywords = sorted(histo.keys(), key=lambda k: histo[k], reverse=True)
    return keywords[0:20]


def extract_key_words_test():
    t = """
The Alien film franchise (also known as Aliens) is a science fiction horror film series consisting of four installments, focusing on Lieutenant Ellen Ripley (Sigourney Weaver) and her battles with an extraterrestrial lifeform, commonly referred to as "the Alien". Produced by 20th Century Fox, the series started with Alien (1979), which led to three movie sequels, as well as numerous books, comics and video game spin-offs.

 prometheus prometheus prometheus prometheus prometheus prometheus

Related to the franchise is the two part Alien vs. Predator series which combines the Aliens with the Predators from the Predator film series. Prometheus, an indirect prequel to Alien released in 2012, is also related.
    """
    print(extract_key_words(t))


def unligaturify(text):
    ligatures = [
        ("db", "ȸ"),
        ("AE", "Æ"),
        ("ae", "æ"),
        ("OE", "Œ"),
        ("oe", "œ"),
        ("ue", "ᵫ"),
        ("ffi", "ﬃ"),
        ("ffl", "ﬄ"),
        ("ff", "ﬀ"),
        ("IJ", "Ĳ"),
        ("ij", "ĳ"),
        ("fi", "ﬁ"),
        ("fl", "ﬂ"),
        ("ft", "ﬅ"),
        ("OI", "Ƣ"),
        ("oi", "ƣ"),
        ("IJ", "Ĳ"),
        ("ij", "ĳ"),
        ("qp", "ȹ"),
        ("st", "ﬆ"),
        ("ſt", "ﬆ"),
    ]

    additional_ligatures = [
        ("et", "&"),
        ("SS", "ẞ"),
        ("ss", "ß"),
    ]

    digraphs = [
        ("DZ", "Ǳ"),
        ("Dz", "ǲ"),
        ("dz", "ǳ"),
        ("DŽ", "Ǆ"),
        ("Dž", "ǅ"),
        ("dž", "ǆ"),
        ("LJ", "Ǉ"),
        ("Lj", "ǈ"),
        ("lj", "ǉ"),
        ("NJ", "Ǌ"),
        ("Nj", "ǋ"),
        ("nj", "ǌ"),
    ]
    for replacement_list in [ligatures, digraphs]:
        for replacement, letters in replacement_list:
            text = text.replace(letters, replacement)
    return text

if __name__ == "__main__":
    print("lib is not a standalone module")
    exit(-1)
