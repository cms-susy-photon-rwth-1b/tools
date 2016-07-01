#!/usr/bin/env python2
"""
Script to merge all files of a directory on Tier2.
usage ./mergeTier2Files.py <outputFile>.root <srm-source-path>
- <srm-source-path> has to be of the form:
  "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/<...>/<date>_<time>/"
  the "<date>_<time>" directory contains numbered directries "0001","0002",... that contain the root files
example usage:
./mergeTier2Files.py out.root srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/jolange/data/Test/GJets_HT-400to600_Tune4C_13TeV-madgraph-tauola/sizeCheck/150504_120017/
"""
import subprocess as sp
import sys
import argparse
import separateSignalPoints as ssp
import os.path

def mergeFiles(inputFiles,outputFile):
    """
    - uses "hadd" to add all inputFiles
    - prepends xrootd-prefixes for remote access
    - merge result is written to outputFile
    """
    # add prefix to access remotely
    gridPrefix="root://xrootd-cms.infn.it//"
    inputFiles = [gridPrefix+f for f in inputFiles]
    if "SMS-T" in inputFiles[0]:
        ssp.separateSignalPoints(inputFiles,os.path.dirname(outputFile))
        return
    print "using hadd to merge",len(inputFiles),"files..."
    if sp.call(["hadd","-v","0","-f",outputFile]+inputFiles):
        sys.exit(1)
    print "written",outputFile

def getDirectoryContent(srmDirectoryPath):
    """
    - returns a list of all files and directories contained in a directory
    - srmDirectoryPath has to be a srm-syntax path
    - returned paths start from '/pnfs/'
    """
    # get srmls output
    contents=sp.check_output(["srmls",srmDirectoryPath])
    # separate output at spaces/line breaks
    contents=contents.split()
    # only every second entry is name, the rest are sizes
    # and the very first entry is the directory name
    contents=contents[3::2]
    # ignore the files placed in the subfolders not containing the
    # relevant data files and the folders themselves
    ignores=("/failed/","/log/")
    contents=[f for f in contents if not f.endswith(ignores)]
    return contents

def getFilePaths(srmDirectoryPath):
    """
    - returns a list of all files contained in a directory
    - srmDirectoryPath has to be a srm-syntax path
    - returned paths start from '/store/'
    """
    files=getDirectoryContent(srmDirectoryPath)
    # extract the relevant part of the paths
    files= ["/store/"+f.partition("/cms/store/")[-1] for f in files if f.endswith(".root")]
    return files


def mergeTier2Files( outputFilePath, inputFilePath, checkDuplicates=False ):
    # get all the subdirectories "/XXXX/" that contain the root files
    dataDirectories=getDirectoryContent(inputFilePath)
    # find all files in these subdirectories
    inputFiles=[]
    for d in dataDirectories:
        inputFiles+=getFilePaths("srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN="+d)

    # merge all of them
    mergeFiles(inputFiles,outputFilePath)

    if checkDuplicates:
        # check if duplicate events exist
        import DuplicateEventFilter.DuplicateEventFilter as dupFilter
        dupFilter.filterFile(outputFilePath,"TreeWriter/eventTree")

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Script to merge all files of a directory on Tier2.")
    parser.add_argument("outFile")
    parser.add_argument("srm_source_path")
    parser.add_argument("-n", "--noDuplicateCheck", action="store_true")
    args = parser.parse_args()

    mergeTier2Files( args.outFile, args.srm_source_path, not args.noDuplicateCheck )
