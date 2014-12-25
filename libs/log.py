#!/usr/bin/env python3
"""
    Logging

    small colored logging functions for python

    author: Steve Göring
    contact: stg7@gmx.de
    2014
"""


def colorred(m):
    return "\033[91m" + m + "\033[0m"


def colorblue(m):
    return "\033[94m" + m + "\033[0m"


def colorgreen(m):
    return "\033[92m" + m + "\033[0m"


def colorcyan(m):
    return "\033[96m" + m + "\033[0m"


def lInfo(msg):
    print(colorgreen("[INFO ] ") + str(msg))


def lError(msg):
    print(colorred("[ERROR] ") + str(msg))


def lDbg(msg):
    print(colorblue("[DEBUG] ") + str(msg))


def lWarn(msg):
    print(colorcyan("[WARN ] ") + str(msg))

if __name__ == "__main__":
    lError("lib is not a standalone module")
    exit(-1)
