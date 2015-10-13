#!/usr/bin/env python2
import ROOT

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.AutoLibraryLoader.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","","HLT")
triggerObjects, triggerObjectLabel  = Handle("std::vector<pat::TriggerObjectStandAlone>"), "selectedPatTrigger"
triggerPrescales, triggerPrescaleLabel  = Handle("pat::PackedTriggerPrescales"), "patTrigger"

events = Events("root://xrootd.unl.edu//store/data/Run2015D/SinglePhoton/MINIAOD/PromptReco-v3/000/256/587/00000/9281243A-945D-E511-96EF-02163E011FBB.root")

myTriggers=[
    "HLT_Photon90_CaloIdL_PFHT500_v",
    "HLT_Photon90_v",
    "HLT_Photon36_R9Id90_HE10_Iso40_EBOnly_PFMET40_v",
    "HLT_Photon36_R9Id90_HE10_Iso40_EBOnly_VBF_v",
    "HLT_Photon50_R9Id90_HE10_Iso40_EBOnly_PFMET40_v",
    "HLT_Photon50_R9Id90_HE10_Iso40_EBOnly_VBF_v",
    "HLT_Photon22_v",
    "HLT_Photon30_v",
    "HLT_Photon36_v",
    "HLT_Photon50_v",
    "HLT_Photon165_R9Id90_HE10_IsoM_v",
    "HLT_Photon36_R9Id90_HE10_IsoM_v",
    "HLT_PFMET170_v"
]
myIndices={}

for iev,event in enumerate(events):
    event.getByLabel(triggerBitLabel, triggerBits)
    event.getByLabel(triggerObjectLabel, triggerObjects)
    event.getByLabel(triggerPrescaleLabel, triggerPrescales)

    names = event.object().triggerNames(triggerBits.product())
    if iev==0:
        # find trigger indices of my triggers
        for i in xrange(triggerBits.product().size()):
            name=names.triggerName(i)
            for myT in myTriggers:
                if name.startswith(myT): myIndices[myT]=i
        print "trigger indices:",myIndices
    # check if my triggers got a prescale
    evtID=(event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
    for myT,myI in myIndices.iteritems():
        presc=triggerPrescales.product().getPrescaleForIndex(myI)
        if presc!=1:
            print "%i:%i:%i"%evtID,myT,"got prescale of",presc
