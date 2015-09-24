#!/usr/bin/env python2

import ROOT
ROOT.gErrorIgnoreLevel=ROOT.kError
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


def readTree( filename, treename ):
    """
    filename: name of file containing the tree
    treename: name of the tree
    returns: TChain Object
    """
    tree = ROOT.TChain( treename )
    tree.AddFile( filename )
    return tree

def filterFile(filename, treename):
   tree = readTree(filename,treename)
   iDoubleEvents=0
   events = set()
   for evt in tree:
      event = Event(evt.runNo, evt.evtNo, evt.lumNo)
      if event in events:
         #print "Event found twice:", event
         iDoubleEvents+=1
      else:
         events.add(event)

   print filename.split('/')[-1],
   if iDoubleEvents>0:
      print "has %d/%d duplicated events"%(iDoubleEvents,tree.GetEntries())
   else:
      print "has NO duplicated events"

if __name__=="__main__":
   filenames=sys.argv[1:]
   for filename in filenames:
      filterFile(filename,"TreeWriter/eventTree")
