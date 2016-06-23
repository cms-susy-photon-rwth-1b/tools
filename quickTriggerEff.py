#!/usr/bin/env python2

# run like ./quickTriggerEff.py /user/lange/data/run2/80X_test_589pbi/JetHT.root

import ROOT as rt
rt.gErrorIgnoreLevel=rt.kError
import sys
from array import array
from collections import defaultdict

def readTree( filename, treename ):
    """
    filename: name of file containing the tree
    treename: name of the tree
    returns: TChain Object
    """
    tree = rt.TChain( treename )
    tree.AddFile( filename )
    return tree

def trigger_eff(filename, treename):
    tree = readTree(filename,treename)

    # eff=rt.TEfficiency("",";pt;eff",100,0,800)
    bins=range(0,160,20)
    bins+=range(160,200,10)
    bins+=range(200,1000,50)
    bins+=range(1000,2000,100)
    bins+=range(2000,4000,250)
    print bins

    runRange=(273100,273800)

    eff=rt.TEfficiency("",";pt;eff",len(bins)-1,array('d',bins))
    mRunTotal=defaultdict(int)
    mRunPass=defaultdict(int)
    for evt in tree:
        pt=-1
        for ph in evt.photons:
            if not ph.hasPixelSeed and abs(ph.p.Eta())<1.4442:
                pt=ph.p.Pt()
                break
        if pt<0: continue

        baseTr=evt.HLT_PFHT125_v or evt.HLT_PFHT200_v or evt.HLT_PFHT250_v or evt.HLT_PFHT300_v or evt.HLT_PFHT350_v or evt.HLT_PFHT400_v or evt.HLT_PFHT475_v or evt.HLT_PFHT600_v or evt.HLT_PFHT650_v or evt.HLT_PFHT800_v
        # baseTr=evt.HLT_PFMET170_NoiseCleaned_v or evt.HLT_PFMET170_HBHECleaned_v or evt.HLT_PFMET170_JetIdCleaned_v or evt.HLT_PFMET170_NotCleaned_v
        sigTr=evt.HLT_Photon165_HE10_v

        if baseTr:
            eff.Fill(sigTr,pt)
            if (pt>180):
                mRunTotal[evt.runNo]+=1
                if (sigTr): mRunPass[evt.runNo]+=1

    can=rt.TCanvas()
    eff.Draw("AP")
    print "pt>%.0f: %.1f+%.1f-%.1f"%(getPlateauEfficiency(eff,180))
    raw_input("...")
    can.Clear()
    eff_run=rt.TEfficiency("effRun",";Run Number;Trigger Efficiency",len(mRunTotal),0,1)
    i=0
    for run in mRunTotal:
        i+=1
        tot=mRunTotal[run]
        pas=mRunPass[run]
        print run,tot,pas
        eff_run.SetTotalEvents (i,tot)
        eff_run.SetPassedEvents(i,pas)

    hDummy=eff_run.GetPassedHistogram().Clone()
    hDummy.Divide(eff_run.GetTotalHistogram())
    hDummy.Draw("axis")
    hDummy.SetMinimum(0)
    hDummy.GetYaxis().SetNdivisions(507)
    hDummy.GetXaxis().SetNdivisions(-1)
    hDummy.GetXaxis().SetTitleOffset(1.5)
    hDummy.GetXaxis().CenterLabels()

    i=0
    for iRun in mRunTotal:
        i+=1
        label="%d"%iRun
        hDummy.GetXaxis().SetBinLabel(i,label);
        print i,label

    effGr=eff_run.CreateGraph()
    effGr.Draw("p")

    raw_input("...")

def getPlateauEfficiency(eff, lower):
    htot=eff.GetCopyTotalHisto()
    hpass=eff.GetCopyPassedHisto()
    lowerBin=htot.FindBin(lower)
    tot=htot.Integral(lowerBin,-1)
    pas=hpass.Integral(lowerBin,-1)
    efficiency=pas/tot
    e_u=rt.TEfficiency.ClopperPearson(int(tot),int(pas),0.682689492137,True)
    e_d=rt.TEfficiency.ClopperPearson(int(tot),int(pas),0.682689492137,False)
    return htot.GetBinLowEdge(lowerBin),efficiency*100, (e_u-efficiency)*100, (efficiency-e_d)*100

if __name__=="__main__":
   analysisDir="/.automount/home/home__home4/institut_1b/lange/ma/analysis"
   rt.gSystem.Load(analysisDir+"/build/lib/libtree.so")
   rt.gROOT.LoadMacro(analysisDir+"/src/style/tdrstyle.C")
   rt.gROOT.Macro(analysisDir+"/src/style/myStyle.C")

   filenames=sys.argv[1:]
   for filename in filenames:
      trigger_eff(filename,"TreeWriter/eventTree")
