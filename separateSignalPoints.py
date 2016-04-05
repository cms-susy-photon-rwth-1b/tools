import ROOT
import os
import re
import subprocess as sp

def randomName():
    # Generate a random string
    from random import randint
    from sys import maxint
    return "%x"%(randint(0, maxint))

def getOutputFilename(outputDir,modelName):
    return "{}/{}__{}.root".format(outputDir,modelName,randomName())

def mergeSignals(outputDir,splitStr="__"):
    import glob
    outFiles=[]
    for file in glob.glob("{}/*{}*.root".format(outputDir,splitStr)):
        if not os.path.exists(file): continue
        m=re.match("(.*){}.*.root".format(splitStr),file)
        if not m: continue
        outFiles.append(m.group(1)+".root")
        sp.call(["hadd -v 0 -f {0}.root {0}{1}*.root".format(m.group(1),splitStr)], shell=True)
        for f in glob.glob("{}{}*.root".format(m.group(1),splitStr)): os.remove(f)
    return outFiles


def attachHistograms(inputFiles,outFiles):
    # write histograms to temporary file
    histFileName="histFiles.root"
    # hadding witout trees, should be pretty fast
    sp.call(["hadd -v 0 -f -T {} {}".format(histFileName," ".join(inputFiles))], shell=True)
    # create dictionary for all histograms in file
    histFile=ROOT.TFile(histFileName)
    hists=dict([(key.GetName(),key.ReadObj()) for key in histFile.GetDirectory("TreeWriter").GetListOfKeys()])
    for fname in outFiles:
        signalPoint=os.path.basename(fname)[:-5] # remove .root
        for name, h in hists.iteritems():
            # search for all histograms containing the model name
            if name.endswith(signalPoint):
                f=ROOT.TFile(fname,"update")
                f.cd("TreeWriter")
                h.Write(name.replace(signalPoint,""))
    # remove temporary file
    os.remove(histFileName)


def separateSignalPoints(inputFiles,outputDir):

    # input tree
    treeName="TreeWriter/eventTree"
    originalChain=ROOT.TChain(treeName)
    for inputFile in inputFiles: originalChain.AddFile(inputFile)

    # separate points
    preModel="" # model of the last event
    for ievent, event in enumerate(originalChain):
        modelName=str(event.modelName)
        if preModel != modelName:
            if preModel: newFile.Write("",ROOT.TObject.kWriteDelete) # not for first event, if no new file exists
            outputFile=getOutputFilename(outputDir,modelName)
            newFile=ROOT.TFile(outputFile,"recreate")
            newFile.mkdir("TreeWriter")
            newFile.cd("TreeWriter")
            newTree=originalChain.CloneTree(0)
            preModel=modelName
        newTree.Fill()
    newFile.Write("",ROOT.TObject.kWriteDelete)

    # merge signal points
    outFiles=mergeSignals(outputDir)

    # write histograms to files
    attachHistograms(inputFiles,outFiles)


