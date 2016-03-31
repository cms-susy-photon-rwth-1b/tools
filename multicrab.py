#!/usr/bin/env python2
import argparse
import subprocess
import os
import glob

import crabInfo

def crabUpdate( dir ):
    # fist check if proxy existent
    out=""
    try:
        out=subprocess.check_output(["voms-proxy-info","--timeleft"],stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        print "Initialize your VOMS proxy!"
        print e.output
        exit(0)
    if int(out)==0:
        print "Your VOMS proxy expired! Please refresh."
        exit(0)
    # try to update
    with open(os.devnull, "w") as FNULL:
        out=subprocess.check_output(["crab","status",dir],stdin=FNULL,stderr=subprocess.STDOUT)
        if "No credentials found!" in out:
            print "No credentials found! Initialize your VOMS proxy."
            exit(0)

def crabResubmit(directory,silent=False):
    with open(os.devnull, "w") as FNULL:
        out=subprocess.check_output(["crab","resubmit",directory],stdin=FNULL,stderr=subprocess.STDOUT)
        if "No credentials found!" in out:
            print "No credentials found! Initialize your VOMS proxy."
            exit(0)
        if not silent: print out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dirs', nargs='+', default=[] )
    parser.add_argument('--noUpdate', action='store_true' )
    parser.add_argument('--autoDL', action='store_true' )
    parser.add_argument('--forceDL', action='store_true' )
    parser.add_argument('--resubmit', action='store_true' )
    args = parser.parse_args()

    dirs = args.dirs or glob.glob(os.environ['CMSSW_BASE']+'/src/TreeWriter/crab/crab_*/')

    for dir in dirs:
        if not args.noUpdate: crabUpdate( dir )
        info = crabInfo.CrabInfo( dir+"/crab.log" )
        if args.resubmit and "failed" in info.details['jobsPerStatus'].keys():
            info.beautifyCrabStatus()
            print "Resubmitting..."
            crabResubmit(dir)
        else:
            info.beautifyCrabStatus()
            if args.forceDL: info.download()
            elif info.completed():
                if args.autoDL: info.download()
                else:           info.suggestMergeCommand()
        print

if __name__ == "__main__":
    main()
