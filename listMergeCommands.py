#!/usr/bin/env python2

import subprocess
import argparse
import re
import getpass

import crabInfo

def getDirs( userInputPath, level=1 ):
    srmlsOut = subprocess.check_output( "srmls -recursion_depth={} srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/{}".format(level, userInputPath), shell=True )

    dirs = []
    for line in srmlsOut.split("\n"):
        match = re.match( "\s*512 (.*)", line )
        if not match: continue
        dirs.append( match.group(1) )
    return dirs



def main():
    parser = argparse.ArgumentParser(description="List posslible merge commands based on the available files.")
    parser.add_argument("--userInputPath", default="")
    args = parser.parse_args()

    if not args.userInputPath:
        user = getpass.getuser()
        if user == "kiesel": args.userInputPath = "kiesel/13TeV/nTuples"
        if user == "jschulz": args.userInputPath = "jschulz/run2"

    dirs = getDirs( args.userInputPath, 4 )

    for line in dirs:
        if not re.match( ".*/([^/]+)/([^/]+)/\d\d\d\d\d\d_\d\d\d\d\d\d/$", line ): continue
        info = crabInfo.CrabInfo( line )
        print info.getMergeCommand()

if __name__ == "__main__":
    main()

