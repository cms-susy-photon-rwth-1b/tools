import FWCore.ParameterSet.Config as cms
process = cms.Process("test")

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    #'root://xrootd-cms.infn.it///store/mc/RunIISpring15MiniAODv2/SMS-T5Wg_mGl-800to1000_mNLSP-0to950_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/70000/F28A96F0-85C5-E511-8812-0025902008AC.root'
    #'root://xrootd-cms.infn.it///store/mc/RunIISpring15MiniAODv2/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/5206D226-316E-E511-A26C-02163E016698.root'
    #'root://xrootd-cms.infn.it///store/mc/RunIISpring16MiniAODv2/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/00000/FAC0A82A-264F-E611-B53F-A0000420FE80.root',
    #'root://xrootd-cms.infn.it///store/mc/RunIISpring16MiniAODv2/ZJetsToNuNu_HT-100To200_13TeV-madgraph/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/90000/F421CA61-BF4D-E611-A192-00259073E544.root',
    #'root://xrootd-cms.infn.it///store/mc/RunIISpring16MiniAODv2/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/60000/F8EE402C-D01B-E611-BECE-0025902BD8CE.root',
    #'root://xrootd-cms.infn.it///store/mc/RunIISpring16MiniAODv2/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/70000/FEF5B630-151D-E611-B26E-002590A831B4.root',
    #'root://xrootd-cms.infn.it///store/mc/RunIISpring16MiniAODv2/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/40000/FECB4924-7925-E611-80F9-0CC47A78A2F6.root',
    'root://xrootd-cms.infn.it///store/mc/RunIISpring16MiniAODv2/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/60000/FC6DE29D-AD1B-E611-8BAD-0025905A6056.root',
    'root://xrootd-cms.infn.it///store/mc/RunIISpring16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/00000/00F0B3DC-211B-E611-A6A0-001E67248A39.root',
    'root://xrootd-cms.infn.it///store/mc/RunIISpring16MiniAODv2/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/90000/DC4900B1-AD51-E611-9F3B-003048344C29.root',
    'root://xrootd-cms.infn.it///store/mc/RunIISpring16MiniAODv2/WGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/10000/FE3031E5-C92B-E611-B6FE-002590E50600.root',
    'root://xrootd-cms.infn.it///store/mc/RunIISpring16MiniAODv2/SMS-T5Wg_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/80000/FEE07B45-8E3E-E611-9287-6C3BE5B5B078.root',
  )
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( 3 )
)

commonSrc = "prunedGenParticles"
#commonSrc = "genParticles"

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")


process.printDecay = cms.EDAnalyzer("ParticleDecayDrawer",
    # seems to be not working
    src = cms.InputTag(commonSrc),
    printP4 = cms.untracked.bool(False),
    printPtEtaPhi = cms.untracked.bool(False),
    printVertex = cms.untracked.bool(False)
)

process.printList = cms.EDAnalyzer("ParticleListDrawer",
    src = cms.InputTag(commonSrc),
    maxEventsToPrint = cms.untracked.int32(-1),
    printVertex = cms.untracked.bool(False),
    printOnlyHardInteraction = cms.untracked.bool(False)
)

process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
    src = cms.InputTag(commonSrc),
    printP4 = cms.untracked.bool(False),
    printPtEtaPhi = cms.untracked.bool(False),
    printVertex = cms.untracked.bool(False),
    printStatus = cms.untracked.bool(False),
    printIndex = cms.untracked.bool(False),
    status = cms.untracked.vint32()
)

process.p = cms.Path(
    process.printDecay \
    * process.printList \
    * process.printTree
)


