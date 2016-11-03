#!/usr/bin/env python2
import argparse
import subprocess
import os
import glob
import re
import ROOT


def getFromFile(filename, objectname):
    f = ROOT.TFile(filename)
    h = f.Get(objectname)
    if not h:
        print "Could not find histogram", objectname, "please consider one of the following points:"
        for k in f.GetDirectory("TreeWriter").GetListOfKeys():
            print k
    h = ROOT.gROOT.CloneObject(h)
    return h

def getCutFlowHistogram(inputFile, point):
    if "SMS-TChi" not in inputFile:
        point = point.replace("gg","Wg").replace("WW", "Wg")
    h = getFromFile(inputFile, "TreeWriter/hCutFlow"+point)
    h.SetName("hCutFlow")
    return h

def getInfoFromPoint(name):
    if name.startswith("TChi"):
        m = re.match("TChi.*_(\d+)", name)
        if not m: print "No Idea what to do with", name
        return m.group(1), 0, 1
    else:
        m = re.match("T\d(.*)_(\d+)_(\d+)", name)
        if not m: print "No Idea what to do with", name
        return m.group(2), m.group(3), m.group(1).count('g')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile")
    parser.add_argument("-p", "--point")
    args = parser.parse_args()

    h = getCutFlowHistogram(args.inputFile, args.point)
    ch = ROOT.TChain("TreeWriter/eventTree")
    ch.AddFile(args.inputFile)
    outputName = os.path.join(os.path.dirname(args.inputFile), "SMS-{}_nTuple.root".format(args.point))
    fout = ROOT.TFile(outputName, "recreate")
    fout.mkdir("TreeWriter")
    fout.cd("TreeWriter")
    m1, m2, nBinos = getInfoFromPoint(args.point)
    new = ch.CopyTree("signal_m1 == {} && signal_m2 == {} && signal_nBinos == {}".format(m1, m2, nBinos))
    new.Write()
    if "T5" or "T6" in args.inputFile:
        # Consider different branching ratio
        if nBinos == 1:
            h.Scale(0.5)
        elif nBinos in [0,2]:
            h.Scale(0.25)
        else:
            print "No idea how to scale cut flow histogram"
    h.Write()
    fout.Close()

