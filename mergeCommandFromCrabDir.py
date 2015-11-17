#!/usr/bin/env python2

import argparse
import re
import getpass
import listMergeCommands

def myMatch( regex, string ):
    m = re.match( regex, string )
    return [ m ] if m else []


def getInfoFromDir( crabDir ):
    if crabDir[-1] != "/": crabDir += "/"
    with open( crabDir+"crab.log" ) as f:
        lines = f.readlines()

    infos = {"crabDir":crabDir}
    for line in lines:
        for m in myMatch("config.Data.outLFNDirBase = '(.*)'", line ):
            infos["lfn"] = m.group(1)
        for m in myMatch( ".*Task name:.*\s([\d_]+):.*_crab_(.*)", line ):
            infos["time"] = m.group(1)
        for m in myMatch( "config.Data.outputDatasetTag = '(.*)'", line ):
            infos["outputDatasetTag"] = m.group(1)
        for m in myMatch( "config.Data.inputDataset = '(.*)'", line ):
            infos["inputDataset"] = m.group(1)
            infos["dset"] = m.group(1).split("/")[1]
            infos["dsetUser"] = infos["dset"]
            for mm in myMatch( '/.*/[^-]*-(.*)-[^-]*/USER', m.group(1) ):
                infos["dsetUser"] = mm.group(1)
            if "Run201" in m.group(1):
                infos["dsetUser"] = "_".join(m.group(1).split("/")[:1])
        if "'schedd'" in line:
            infos.update(eval( line.split("\t")[-1] ))

    return infos

def getOutFileName( infos ):
    user = getpass.getuser()
    if user == "kiesel":
        shotDset = listMergeCommands.modifyDatasetName(infos["dsetUser"])
        return "/user/kiesel/nTuples/{}/{}_nTuple.root".format(infos["outputDatasetTag"],shortDset )
    return "test.root"

def getSrmInput( infos ):
    return "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms{lfn}/{dset}/{outputDatasetTag}/{time}/".format( **infos )


def getMergeCommand( crabDir ):
    infos = getInfoFromDir( crabDir )
    outFile = getOutFileName( infos )
    srmSrc = getSrmInput( infos )
    return "./mergeTier2Files.py {} {}".format(outFile,srmSrc)

def main():
    parser = argparse.ArgumentParser(description="List merge command based on crab directory.")
    parser.add_argument("crabDirs", nargs="+" )
    args = parser.parse_args()

    for crabDir in args.crabDirs:
        print getMergeCommand( crabDir )


if __name__ == "__main__":
    main()

