#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ROOT
import argparse
import matplotlib.pyplot as plt

def printTreeSize(filename, treename):
    t = ROOT.TChain(treename)
    t.AddFile(filename)
    branchSizes = []
    for b in t.GetListOfBranches():
        branchSizes.append( (b.GetName(), b.GetTotalSize()) )
    branchSizes = sorted(branchSizes, key=lambda x: x[1], reverse=True)
    maxWidthEntry = max(branchSizes, key=lambda x: len(x[0])+len(str(x[1]))+1)
    width = len(maxWidthEntry[0]) + len(str(maxWidthEntry[1]))
    for a,b in branchSizes: print a, " "*(width-len(a)-len(str(b))), b

    # draw it
    labels = [a for a,b in branchSizes]
    sizes = [b for a,b in branchSizes]
    fig = plt.figure()
    ax = fig.gca()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, radius=1)
    plt.show()
    plt.savefig('treeSize.pdf')
    print "Saved to: treeSize.pdf"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--tree", default="TreeWriter/eventTree")
    args = parser.parse_args()

    printTreeSize(args.file, args.tree)


