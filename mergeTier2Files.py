#!/usr/bin/env python27
"""
Script to merge all files of a directory on Tier2.
example usage:
./mergeTier2Files.py out.root srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/jolange/data/Test/Test/GJet_Pt40_doubleEMEnriched_TuneZ2star_13TeV-pythia6//CAB3-test/150504_071807/0000
"""
import subprocess as sp
import sys

def mergeFiles(inputFiles,outputFile):
    """
    - uses "hadd" to add all inputFiles
    - prepends xrootd-prefixes for remote access
    - merge result is written to outputFile
    """
    # add prefix to access remotely
    gridPrefix="root://xrootd-cms.infn.it//"
    inputFiles = [gridPrefix+f for f in inputFiles]
    print "using hadd to merge",len(inputFiles),"files..."
    sp.call(["hadd","-v","0","-f","test.root"]+inputFiles)
    print "written",outputFile

def getFilePaths(srmDirectoryPath):
    """
    - returns a list of all files contained in a directory
    - srmDirectoryPath has to be a srm-syntax path
    - returned paths start from '/store/'
    """
    # get srmls output
    files=sp.check_output(["srmls",srmDirectoryPath])
    # separate output at spaces/line breaks
    files=files.split()
    # only every second entry is name, the rest are sizes
    # and the very first entry is the directory name
    files=files[3::2]
    # extract the relevant part of the paths
    files= ["/store/"+f.partition("/cms/store/")[-1] for f in files]
    return files
    
if __name__=="__main__":
    outputFile=""
    nextIsOutputName=False
    # read input and output from arguments
    if len(sys.argv) != 3:
        print "usage:",sys.argv[0],"<outputFile>.root <srm-source-path>"
        exit(0)
    inputFilePath =sys.argv[2]
    outputFilePath=sys.argv[1]
    # find all input files
    inputFiles=getFilePaths(inputFilePath)
    # merge them
    mergeFiles(inputFiles,outputFilePath)
