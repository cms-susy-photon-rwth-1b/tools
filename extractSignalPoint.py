#!/usr/bin/env python2
import argparse
import subprocess
import os
import glob
import re
import ROOT
import getpass
import sys


def getFromFile(filename, objectname):
    f = ROOT.TFile(filename)
    h = f.Get(objectname)
    if not h:
        print "Could not find histogram", objectname, "please consider one of the following points:"
        names = [k.GetName() for k in f.GetDirectory("TreeWriter").GetListOfKeys()]
        print "\n".join(sorted(names))
        sys.exit(1)
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
    parser = argparse.ArgumentParser(description="Example: ./extractSignalPoint.py ~/nTuples/SMS-T5Wg_nTuple.root -p T5Wg_1600_1500")
    parser.add_argument("inputFile")
    parser.add_argument("-p", "--point")
    args = parser.parse_args()

    h = getCutFlowHistogram(args.inputFile, args.point)
    ch = ROOT.TChain("TreeWriter/eventTree")
    ch.AddFile(args.inputFile)
    user = getpass.getuser()
    if user == "jschulz" or user == "dmeuser":
        outputName = os.path.join(os.path.dirname(args.inputFile), "{}.root".format(args.point))
    elif user == "kiesel":
        outputName = os.path.join(os.path.dirname(args.inputFile), "SMS-{}_nTuple.root".format(args.point))
    elif user == "swuchterl":
        outputName = os.path.join(os.path.dirname(args.inputFile), "SMS-{}_nTuple.root".format(args.point))
    else:
        print "ERROR: unknown user"
    fout = ROOT.TFile(outputName, "recreate")
    fout.mkdir("TreeWriter")
    fout.cd("TreeWriter")
    m1, m2, nBinos = getInfoFromPoint(args.point)
    cutString = "signal_m1 == {} && signal_m2 == {}".format(m1, m2)
    if ("T5" in args.inputFile or "T6" in args.inputFile) and nBinos != 1:
        cutString += " && signal_nBinos == {}".format(nBinos)
        h.Scale(0.25)
    new = ch.CopyTree(cutString)
    new.Write("", ROOT.TObject.kWriteDelete)
    h.Write()
    fout.Close()


