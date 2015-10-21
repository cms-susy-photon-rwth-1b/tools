#!/usr/bin/env python2

import argparse
import re

def getInfoFromDir( crabDir ):
    if crabDir[-1] != "/": crabDir += "/"
    with open( crabDir+"crab.log" ) as f:
        lines = f.readlines()

    infos = {}

    for line in lines:
        m1 = re.match("config.Data.outLFNDirBase = '(.*)'", line )
        if m1:
            infos["lfn"] = m1.group(1)
        m2 = re.match( ".*Task name:.*\s([\d_]+):.*_crab_(.*)", line )
        if m2 and "time" not in infos:
            infos["time"] = m2.group(1)
            infos["dset"] = m2.group(2)
        m3 = re.match( "config.Data.publishDataName = '(.*)'", line )
        if m3:
            infos["publishDataName"] = m3.group(1)

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

