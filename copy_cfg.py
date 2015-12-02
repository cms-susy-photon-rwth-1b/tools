# This script copies nEvents events from a file
# from some T2 to your local disk and names it wisely
# You should only use this for testing

# Usage: cmsRun copy_cfg.py inputFiles=/store/data/...root [maxEvents=50]
# or     cmsRun copy_cfg.py dataset=/SinglePhoton/Run2015D-PromptReco-v4/MINIAOD
#options.inputFiles = "/store/mc/Fall13dr/QCD_Pt-170to300_Tune4C_13TeV_pythia8/GEN-SIM-RAW/castor_tsg_PU40bx25_POSTLS162_V2-v1/00000/001B2136-7AA6-E311-9C66-002618943939.root"


import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing


def getFilesFromDataset( dataset ):
    import subprocess
    a = subprocess.check_output("das_client.py --limit 0 --query 'file dataset=%s'"%dataset, shell=True )
    lines = a.split("\n")[:-1]
    return lines

def getOutputNameFromDataset( dataset, dir="/user/kiesel/root-files/" ):
    return dir+'_'.join(dataset.split("/")[1:])+".root"

def getOutputNameFromFile( filename, dir="/user/kiesel/root-files/" ):
    s = filename.split("/")
    return dir+'_'.join([s[4],s[6],s[5]])+".root"

options = VarParsing.VarParsing ('analysis')
options.maxEvents = 5
options.register ('dataset','',VarParsing.multiplicity.singleton,VarParsing.varType.string)
options.parseArguments()


files = []
outName = "test.root"
if options.dataset:
    files = getFilesFromDataset( options.dataset )
    outName = getOutputNameFromDataset( options.dataset )
if options.inputFiles:
    files = options.inputFiles
    outName = getOutputNameFromFile( options.inputFiles[0] )


process = cms.Process('COPY')

process.source = cms.Source( "PoolSource",
    fileNames = cms.untracked.vstring( [ "root://xrootd-cms.infn.it/"+x for x in files ] ),
    #eventsToProcess = cms.untracked.VEventRange('191226:396072909-191226:396072909')
    #eventsToProcess = cms.untracked.VEventRange('194429:390:367456133-194429:390:367456133','206302:74:120668722-206302:74:120668722' ) # high met events
    )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32( options.maxEvents ) )

process.output = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring("keep *"),
    fileName = cms.untracked.string(outName),
)

process.out_step = cms.EndPath(process.output)
