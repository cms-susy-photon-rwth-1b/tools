#!/usr/bin/env python2
import ROOT as rt
import sys
if __name__ == '__main__':
    filename=sys.argv[1]
    rt.gStyle.SetNdivisions(50,"xy")

    f=rt.TFile(filename,"read")
    if "MINIAODSIM" in filename:
        tree=f.Get("Events")
        pdgId="recoGenParticles_prunedGenParticles__PAT.obj.m_state.pdgId_"
    elif "AODSIM" in filename:
        tree=f.Get("Events")
        pdgId="recoGenParticles_genParticles__HLT.obj.m_state.pdgId_"
    else:
        # try local trees
        tree=f.Get("TreeWriter/eventTree") # 13 TeV trees
        if not tree:
            tree=f.Get("susyTree") # 8 TeV trees
        pdgId="genParticles.pdgId"

    can=rt.TCanvas()
    can.Divide(1,2)
    can.cd(1)
    rt.gPad.SetLogy()
    tree.Draw(pdgId+"-1000000>>h1(50,0.5,50.5)",pdgId+">1e6 &&"+pdgId+"<1.1e6")
    rt.gDirectory.Get("h1").SetTitle(";pdgId-1e6;")
    can.cd(2)
    rt.gPad.SetLogy()
    tree.Draw(pdgId+"-2000000>>h2(50,0.5,50.5)",pdgId+">2e6 &&"+pdgId+"<2.1e6")
    rt.gDirectory.Get("h2").SetTitle(";pdgId-2e6;")

    raw_input("...")
    f.Close()
