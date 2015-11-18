#!/usr/bin/env python2
import argparse
import subprocess
import os
import glob

import crabInfo

def crabUpdate( dir ):
    subprocess.call( "crab status {} > /dev/zero".format(dir), shell=True )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dirs', nargs='+', default=[] )
    parser.add_argument('--noUpdate', action='store_true' )
    parser.add_argument('--auto', action='store_true' )
    args = parser.parse_args()

    dirs = args.dirs or glob.glob(os.environ['CMSSW_BASE']+'/src/TreeWriter/crab/crab_*/')

    for dir in dirs:
        if not args.noUpdate: crabUpdate( dir )
        info = crabInfo.CrabInfo( dir+"/crab.log" )
        info.beautifyCrabStatus(args.auto)


if __name__ == "__main__":
    main()
