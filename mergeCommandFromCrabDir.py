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
    parser.add_argument('--joFormat',dest="joFormat", action='store_const',const=True,default=False,
                        help="Johannes' output format")

    args = parser.parse_args()

    infos = getInfoFromDir( args.crabDir )
    if not args.joFormat:
        infos["out"] = args.out
        infos["mergeCommand"]="./mergeTier2Files.py"
    else:
        from listMergeCommands import modifyDatasetName
        outFileName=args.crabDir[:-1]
        outFileName=modifyDatasetName(outFileName.replace("crab_",""))
        infos["out"] = "/user/lange/data/run2/dl/"+outFileName+".root"
        infos["mergeCommand"]="mergeTier2Files.py"

    print "{mergeCommand} {out} srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms{lfn}/{dset}/{publishDataName}/{time}/".format( **infos )

if __name__ == "__main__":
    main()

