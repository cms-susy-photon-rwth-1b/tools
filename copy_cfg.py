# This script copies nEvents events from a file
# from some T2 to your local disk and names it wisely
# You should only use this for testing

# Usage: cmsRun copy_cfg.py inputFiles=/store/data/...root [maxEvents=50]
# or     cmsRun copy_cfg.py dataset=/SinglePhoton/Run2015D-PromptReco-v4/MINIAOD
#options.inputFiles = "/store/mc/Fall13dr/QCD_Pt-170to300_Tune4C_13TeV_pythia8/GEN-SIM-RAW/castor_tsg_PU40bx25_POSTLS162_V2-v1/00000/001B2136-7AA6-E311-9C66-002618943939.root"


import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import getpass

def getFilesFromDataset( dataset ):
    import subprocess
    a = subprocess.check_output("das_client.py --limit 0 --query 'file dataset=%s'"%dataset, shell=True )
    lines = a.split("\n")[:-1]
    return lines

def getOutputNameFromDataset( dataset, dir ):
    return dir+'_'.join(dataset.split("/")[1:])+".root"

def getOutputNameFromFile( filename, dir ):
    s = filename.split("/")
    return dir+'_'.join([s[4],s[6],s[5]])+".root"

options = VarParsing('analysis')
options.maxEvents = 5
options.register ('dataset','',VarParsing.multiplicity.singleton,VarParsing.varType.string)
options.parseArguments()

user=getpass.getuser()
dir="./"
if user=="kiesel":
    dir="/user/kiesel/root-files/"
else:
    print "Unknown user", user

files = []
outName = "test.root"
if options.dataset:
    files = getFilesFromDataset( options.dataset )
    outName = getOutputNameFromDataset( options.dataset, dir )
if options.inputFiles:
    files = options.inputFiles
    outName = getOutputNameFromFile( options.inputFiles[0], dir )


process = cms.Process('COPY')

process.source = cms.Source( "PoolSource",
    fileNames = cms.untracked.vstring( [ "root://xrootd-cms.infn.it/"+x for x in files ] ),
    #eventsToProcess = cms.untracked.VEventRange('191226:396072909-191226:396072909')
    #eventsToProcess = cms.untracked.VEventRange('194429:390:367456133-194429:390:367456133','206302:74:120668722-206302:74:120668722' ) # high met events
    #eventsToProcess = cms.untracked.VEventRange( "284043:13:19552168", "284043:19:29958410", "284037:208:388816811", "284037:47:89505912", "284036:51:90938369", "284042:38:59468321", "284036:124:215469987", "284036:206:358595681", "284036:321:566607039", "284036:338:594546722", "284036:342:601587292")
    #eventsToProcess = cms.untracked.VEventRange("274241:701:1168245835","273158:735:1082399606","274244:601:863108399","275001:720:1033007773","275371:304:599848939","274388:1428:2559723415","275068:654:1218063346","275890:807:1560972365","275890:1252:2352827897","275836:264:510699871","276242:1378:2574937437","276794:603:800050435","276810:24:43597044","276581:124:125102144","276653:347:524088690","277194:660:1085910298","277096:373:678913025","277168:2103:3674985444","276831:943:1699698783","277168:1681:3040714738","276935:484:737036208","277305:412:640557367","277420:344:521100446","276870:3235:5635144866","277070:799:1474993474","278018:328:610192996","278770:170:331639831","279844:233:297252381","279716:1104:1960082201","279931:2828:4832376009","279715:351:532551390","279966:194:239850867","278975:534:839046791","278969:467:733491516","279841:320:489651116","280349:51:95527167","283885:1212:2145998961","283283:466:943827015","283308:134:253646428","282735:1590:2961719613","283820:232:393031344","283353:161:169955262","283876:200:262510838","284014:15:26409825") #johannes st>1300
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32( options.maxEvents ) )

process.output = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring("keep *"),
    fileName = cms.untracked.string(outName),
)

process.out_step = cms.EndPath(process.output)
