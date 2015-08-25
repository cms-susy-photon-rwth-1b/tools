#!/usr/bin/env python

import subprocess
import argparse
import re


def modifyDatasetName( dataset ):
    # shorten dataset name
    deletes = [ "_13TeV", "-madgraph", "_Tune4C", "-tauola", "_MSDecaysCKM_central", "_TuneCUETP8M1", "-amcatnloFXFX", "-madspin", "-pythia8" ]
    for d in deletes:
        dataset = dataset.replace( d, "" )
    return dataset

def main():
    parser = argparse.ArgumentParser(description="List posslible merge commands based on the available files.")
    parser.add_argument("--userInputPath", default="kiesel/13TeV/nTuples")
    parser.add_argument("--outputPath", default="/user/kiesel/nTuples")
    parser.add_argument("--srmPrefix", default="srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=")
    args = parser.parse_args()

    srmlsOut = subprocess.check_output( "srmls -recursion_depth=5 {}/pnfs/physik.rwth-aachen.de/cms/store/user/{}".format(args.srmPrefix,args.userInputPath), shell=True )
    for line in srmlsOut.split("\n"):
        match = re.match( ".*/([^/]+)/.*/\d\d\d\d\d\d_\d\d\d\d\d\d/$", line )
        if match:
            dataset = match.groups()[0]
            inFolder = line.replace("512", "").strip()
            dataset = modifyDatasetName( dataset )
            print "./mergeTier2Files.py %s/%s_nTuple.root %s%s"%(args.outputPath,dataset,args.srmPrefix,inFolder)

if __name__ == "__main__":
    main()

