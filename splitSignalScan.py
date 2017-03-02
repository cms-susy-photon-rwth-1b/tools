#!/usr/bin/env python2
import argparse
import os
import ROOT

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile")
    args = parser.parse_args()

    f = ROOT.TFile(args.inputFile)
    hists = []
    for key in f.GetDirectory("TreeWriter").GetListOfKeys():
        h = key.ReadObj()
        if not isinstance(h, ROOT.TH1): continue
        h.SetDirectory(0)
        hists.append(h)

    ch = ROOT.TChain("TreeWriter/eventTree")
    ch.AddFile(args.inputFile)

    outputName = os.path.join(args.inputFile.replace(".root", "_gg.root"))
    fout = ROOT.TFile(outputName, "recreate")
    fout.mkdir("TreeWriter")
    fout.cd("TreeWriter")
    new = ch.CopyTree("signal_nBinos == 2")
    new.Write("", ROOT.TObject.kWriteDelete)
    for h in hists: h.Write()
    fout.Close()
    print "Created", outputName

    outputName = os.path.join(args.inputFile.replace(".root", "_Wg.root"))
    fout = ROOT.TFile(outputName, "recreate")
    fout.mkdir("TreeWriter")
    fout.cd("TreeWriter")
    new = ch.CopyTree("signal_nBinos == 1")
    new.Write("", ROOT.TObject.kWriteDelete)
    for h in hists: h.Write()
    fout.Close()
    print "Created", outputName



