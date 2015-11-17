#!/usr/bin/env python2

import subprocess
import argparse
import re


def modifyDatasetName( dataset ):
    # shorten dataset name
    deletes = [ "_13TeV", "-madgraph", "_Tune4C", "-tauola", "_MSDecaysCKM_central", "_TuneCUETP8M1", "-amcatnloFXFX", "-madspin", "-pythia8", "MLM", "_pythia8" ]
    for d in deletes:
        dataset = dataset.replace( d, "" )
    return dataset


def getDirs( args, level=1 ):
    srmlsOut = subprocess.check_output( "srmls -recursion_depth={} {}/pnfs/physik.rwth-aachen.de/cms/store/user/{}".format(level, args.srmPrefix,args.userInputPath), shell=True )

    dirs = []
    for line in srmlsOut.split("\n"):
        match = re.match( "\s*512 (.*)", line )
        if not match: continue
        dirs.append( match.group(1) )
    return dirs





def main():
    parser = argparse.ArgumentParser(description="List posslible merge commands based on the available files.")
    parser.add_argument("--userInputPath", default="kiesel/13TeV/nTuples")
    parser.add_argument("--outputPath", default="/user/kiesel/nTuples")
    parser.add_argument("--srmPrefix", default="srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=")
    parser.add_argument('--joFormat',dest="joFormat", action='store_const',const=True,default=False,
                        help="Johannes' output format")
    args = parser.parse_args()

    dirs = getDirs( args, 4 )

    for line in dirs:
        match = re.match( ".*/([^/]+)/([^/]+)/\d\d\d\d\d\d_\d\d\d\d\d\d/$", line )
        if not match: continue
        dataset, publishedName = match.groups()
        inFolder = line.replace("512", "").strip()
        dataset = modifyDatasetName( dataset )
        if not args.joFormat:
            print "./mergeTier2Files.py %s/%s_%s_nTuple.root %s%s"%(args.outputPath,dataset,publishedName,args.srmPrefix,inFolder)
        else:
            print "./mergeTier2Files.py %s/%s.root %s%s"%("/user/lange/data/run2/dl",dataset,args.srmPrefix,inFolder)

if __name__ == "__main__":
    main()

