#!/usr/bin/env python2

import argparse
import re

def myMatch( regex, string ):
    m = re.match( regex, string )
    return [ m ] if m else []


def getInfoFromDir( crabDir ):
    if crabDir[-1] != "/": crabDir += "/"
    with open( crabDir+"crab.log" ) as f:
        lines = f.readlines()

    infos = {}

    for line in lines:
        for m in myMatch("config.Data.outLFNDirBase = '(.*)'", line ):
            infos["lfn"] = m.group(1)
        for m in myMatch( ".*Task name:.*\s([\d_]+):.*_crab_(.*)", line ):
            infos["time"] = m.group(1)
        for m in myMatch( "config.Data.publishDataName = '(.*)'", line ):
            infos["publishDataName"] = m.group(1)
        for m in myMatch( "config.Data.inputDataset = '/([^/]*)/.*'", line ):
            infos["dset"] = m.group(1)

    return infos


def main():
    parser = argparse.ArgumentParser(description="List merge command based on crab directory.")
    parser.add_argument("crabDir")
    parser.add_argument( "-o", "--out", default="test.root")
    args = parser.parse_args()

    infos = getInfoFromDir( args.crabDir )
    infos["out"] = args.out

    print "./mergeTier2Files.py {out} srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms{lfn}/{dset}/{publishDataName}/{time}/".format( **infos )

if __name__ == "__main__":
    main()

