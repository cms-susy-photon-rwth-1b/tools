#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import subprocess

saveFile = "datasetsMoriond17.txt"

def getDasOutput():
    out = subprocess.check_output(['das_client --query="dataset=/*/*Moriond17*/MINIAOD*" --limit=0 | sort'], shell=True)
    return out

def getDatasets(out):
    return out.split("\n")

if __name__ == "__main__":
    if os.path.isfile(saveFile):
        with open(saveFile) as f:
            oldDatasets = getDatasets(f.read())
    else:
        oldDatasets = []
    newOut = getDasOutput()
    actualDatasets = getDatasets(newOut)
    newDatasets = [ x for x in actualDatasets if x not in oldDatasets]
    print "New datasets:"
    print "\n".join(newDatasets)
    with open(saveFile, "w+") as f:
        f.write(newOut)

