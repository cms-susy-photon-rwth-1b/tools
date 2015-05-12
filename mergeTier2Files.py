#!/usr/bin/env python27

import subprocess as sp

def mergeFiles(inputFiles):
    """
    - uses "hadd" to add all inputFiles
    - prepends xrootd-prefixes for remote access
    """
    # add prefix to access remotely
    gridPrefix="root://xrootd-cms.infn.it//"
    inputFiles = [gridPrefix+f for f in inputFiles]
    
    sp.call(["hadd","-f","test.root"]+inputFiles)

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
    inputFiles=getFilePaths("srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/jolange/data/Test/Test/GJet_Pt40_doubleEMEnriched_TuneZ2star_13TeV-pythia6//CRAB3-test/150504_071807/0000/")
    mergeFiles(inputFiles)
