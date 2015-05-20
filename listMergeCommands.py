#!/usr/bin/env python

import subprocess


def modifyDatasetName( dataset ):
    # shorten dataset name
    deletes = [ "_13TeV", "-madgraph", "_Tune4C", "-tauola" ]
    for d in deletes:
        dataset = dataset.replace( d, "" )
    return dataset

def main():
    srmPrefix = "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN="
    user = "jolange"
    outputPath = "/user/kiesel/nTuples/"

    srmlsOut = subprocess.check_output( "srmls -recursion_depth=5 {}/pnfs/physik.rwth-aachen.de/cms/store/user/{}/".format(srmPrefix,user), shell=True )
    for line in srmlsOut.split("\n"):
        if "                   " in line:

            inFolder = line.split(" ")[-1]
            dataset = inFolder.split("/")[9]
            dataset = modifyDatasetName( dataset )
            print "./mergeTier2Files.py %s/%s_nTuple.root %s%s"%(outputPath,dataset,srmPrefix,inFolder)

if __name__ == "__main__":
    main()

