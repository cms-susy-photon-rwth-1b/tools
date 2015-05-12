#!/usr/bin/env python2

import subprocess as sp

def mergeFiles(inputFiles):
    # add prefix to access remotely
    gridPrefix="root://xrootd-cms.infn.it//"
    inputFiles = [gridPrefix+f for f in inputFiles]
    
    sp.call(["hadd","-f","test.root"]+inputFiles)

if __name__=="__main__":
    inputFiles=[
        "/store/user/jolange/data/Test/Test/GJet_Pt40_doubleEMEnriched_TuneZ2star_13TeV-pythia6//CRAB3-test/150504_071807/0000/photon_ntuple_mva_mini_38.root",
        "/store/user/jolange/data/Test/Test/GJet_Pt40_doubleEMEnriched_TuneZ2star_13TeV-pythia6//CRAB3-test/150504_071807/0000/photon_ntuple_mva_mini_36.root"
    ]
    mergeFiles(inputFiles)
