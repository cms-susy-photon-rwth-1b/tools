#!/usr/bin/env python

import subprocess
import time

def getInfos():
    out = subprocess.check_output(["condor_q", "-long"])
    for jobStrings in out.split("\n\n"):
        for line in jobStrings.split("\n"):
            if line:
                break
                print [line.split(" = ")]
    return [ dict([line.replace("\"","").split(" = ") for line in jobStrings.split("\n") if " = " in line]) for jobStrings in out.split("\n\n") if jobStrings ]

def getSummary():
    out = subprocess.check_output(["condor_q"])
    return out.split("\n")[-2]

def getNameFromFile(fname):
    return fname.split("/")[-1].replace("_nTuple.root","").split(" ")[0]

jobs = getInfos()

for job in jobs:
    name = getNameFromFile(job["Args"])
    name += " "*max([0,(40-len(name))])
    if job['JobStatus'] == '2':
        print name, "running"
    else:
        susTime = (time.time()-int(job["LastSuspensionTime"]))/60.
        print name, "suspended since", susTime, "min"
print getSummary()

