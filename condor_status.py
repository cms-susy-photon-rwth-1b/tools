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
jobs = sorted(jobs, key=lambda l: l["JobStatus"]+l["Args"])

for job in jobs:
    name = getNameFromFile(job["Args"])
    name += " "*max([0,(40-len(name))])
    jStatus = job["JobStatus"]
    if jStatus == "1":
        print name, "idle"
    elif jStatus == "2":
        print name, "running"
    elif jStatus == "7":
        susTime = (time.time()-int(job["LastSuspensionTime"]))/60.
        print name, "suspended since {:.2f} min".format(susTime)
    else:
        print "job status = ", jStatus
print getSummary()

