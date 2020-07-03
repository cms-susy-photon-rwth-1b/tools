#!/usr/bin/env python

import subprocess
import time
import os

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
jobs = sorted(jobs, key=lambda l: l["JobStatus"]+l["ClusterId"])
susJobs = []

for job in jobs:
    if job["Cmd"].split("/")[-1]=="run.sh":
        name = getNameFromFile(job["Args"])
    else:
        name = (job["Args"].split(",")[0]).split("/")[2]
    name += " "*max([0,(40-len(name))])
    jStatus = job["JobStatus"]
    if jStatus == "1":
        print name, job["ClusterId"], "       idle"
    elif jStatus == "2":
        print name, job["ClusterId"], "       running"
    elif jStatus == "5":
        print name, job["ClusterId"], "       held"
    elif jStatus == "7":
        susTime = (time.time()-int(job["LastSuspensionTime"]))/60.
        print name, job["ClusterId"], "       suspended since {:.2f} min".format(susTime), "         "+job["RemoteHost"]
        if susTime > 10 :
            susJobs.append(job["ClusterId"])
    else:
        print "job status = ", jStatus
print getSummary()
for job in susJobs:
    os.system("condor_hold "+job)
if len(susJobs)!=0: os.system("condor_release dmeuser")

