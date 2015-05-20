#!/usr/bin/env python2

import ROOT
import sys


class Event():
   def __init__(self, runNo, evtNo, lumNo):
      self.runNo=runNo
      self.evtNo=evtNo
      self.lumNo=lumNo

   def __eq__(self,other):
      if isinstance(other,self.__class__):
         return self.runNo == other.runNo and self.evtNo == other.evtNo and self.lumNo == other.lumNo
      else:
         return False
   def __ne__(self,other):
      return not self.__eq__(other)

   def __hash__(self):
      return self.evtNo

   def __str__(self):
      return "(r%d, e%d, l%d)"%(self.runNo,self.evtNo,self.lumNo)


def readTree( filename, treename = "susyTree" ):
    """
    filename: name of file containing the tree
    treename: name of the tree
    returns: TChain Object
    """
    tree = ROOT.TChain( treename )
    tree.AddFile( filename )
    return tree

def filterFile(filename):
   tree = readTree(filename)
   iDoubleEvents=0
   events = set()
   for evt in tree:
      event = Event(evt.runNumber, evt.eventNumber, evt.luminosityBlockNumber)
      if event in events:
         #print "Event found twice:", event
         iDoubleEvents+=1
      else:
         events.add(event)

   if iDoubleEvents>0:
      print filename.split('/')[-1],
      print "double events: %d/%d"%(iDoubleEvents,tree.GetEntries())

if __name__=="__main__":
   ROOT.gErrorIgnoreLevel=ROOT.kError

   dCachePrefix = "dcap://dcache-cms-dcap.desy.de"
   filenames=sys.argv[1:]
   for filename in filenames:
      filterFile(dCachePrefix+filename)
