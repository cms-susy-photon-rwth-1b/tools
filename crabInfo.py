import re
import getpass
from CRABClient.ClientUtilities import colors
import mergeTier2Files

def myMatch( regex, string ):
    m = re.match( regex, string )
    return [ m ] if m else []

def modifyDatasetName( dataset ):
    # shorten dataset name
    deletes = [
        "_13TeV",
        "-madgraph",
        "_Tune4C",
        "-tauola",
        "_MSDecaysCKM_central",
        "_TuneCUETP8M1",
        "-amcatnloFXFX",
        "-madspin",
        "-pythia8",
        "MLM",
        "_pythia8"
    ]
    if dataset.startswith("WGToLNuG_"):
        # to be able to seperate these two datasets
        deletes.remove( "-amcatnloFXFX" )
        deletes.remove( "-madgraph" )
        deletes.remove( "MLM" )
    for d in deletes:
        dataset = dataset.replace( d, "" )
    return dataset

class CrabInfo:

    def __init__( self, infoString ):

        if infoString.endswith("/crab.log"):
            self.initFromLog( infoString )
        elif "/pnfs/physik.rwth-aachen.de/cms/store" in infoString:
            self.initFromSrm( infoString )

    def initFromLog( self, logFileName ):
        self.logFileDir = logFileName.replace("/crab.log","")

        with open( logFileName ) as f:
            lines = f.readlines()

        for line in lines:
            for m in myMatch("config.Data.outLFNDirBase = '(.*)'", line ):
                self.outLFNDirBase = m.group(1)
            for m in myMatch( ".*Task name:.*\s([\d_]+):.*_crab_(.*)", line ):
                self.time = m.group(1)
            for m in myMatch( "config.Data.outputDatasetTag = '(.*)'", line ):
                self.outputDatasetTag = m.group(1)
            for m in myMatch( "config.Data.inputDataset = '(.*)'", line ):
                self.inputDataset = m.group(1)
                self.datasetName, self.datasetMiddle, self.datasetType = self.inputDataset.split("/")[1:]
            if "'schedd'" in line:
                self.details = eval( line.split("\t")[-1] )

    def initFromSrm( self, srmPath ):
        self.srmPath = srmPath
        srmPathSplitted = srmPath.split("/")
        self.time = srmPathSplitted[-2]
        self.outputDatasetTag = srmPathSplitted[-3]
        self.datasetName = srmPathSplitted[-4]

    def getOutFileName( self ):
        user = getpass.getuser()
        modifiedDatasetName = modifyDatasetName( self.datasetName )
        if user == "kiesel":
            if hasattr(self, "datasetType"):
                if self.datasetType == "MINIAOD": # data
                    modifiedDatasetName += "_"+self.datasetMiddle
                if self.datasetType == "USER": # assume the signal scan
                    for m in myMatch( '/.*/[^-]*-(.*)-[^-]*/USER', self.datasetMiddle ):
                        modifiedDatasetName += "_"+m.groups(1)
            return "/user/kiesel/nTuples/{}/{}_nTuple.root".format( self.outputDatasetTag, modifiedDatasetName )
        elif user == "lange":
            return "/user/lange/data/run2/dl/{}.root".format(modifiedDatasetName)
        elif user == "rmeyer":
            return "my_output_file.root"
        return "outputFile.root"

    def getSrmPath( self ):
        if not hasattr(self, 'srmPath'):
             self.srmPath = "/pnfs/physik.rwth-aachen.de/cms{}/{}/{}/{}/".format(self.outLFNDirBase,self.datasetName,self.outputDatasetTag,self.time)
        return self.srmPath

    def getSrmPathFull( self ):
        return "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN="+self.getSrmPath()

    def jobSummary( self ):

        njobs = len(self.details['jobList'])
        for k,v in self.details['jobsPerStatus'].iteritems():
            c = colors.NORMAL
            if k == "failed": c = colors.RED
            if k == "running": c = colors.GREEN
            if k == "transferrig": c = colors.BLUE
            print "{}\t{}{}  \t{:.1%} ({}{:3}{}/{:3})".format(c,k,colors.NORMAL,1.*v/njobs,c,v,colors.NORMAL,njobs)

        """# TODO: nice error output
        for j, d in self.details["jobs"].iteritems():
            if d["State"] == "failed":
                for i in d["Error"]:
                    try:
                        if "code" in i: print i
                    except: pass
        """

    def getMergeCommand( self ):
        outFile = self.getOutFileName()
        srmSrc  = self.getSrmPathFull()
        return "./mergeTier2Files.py {} {}".format(outFile,srmSrc)


    def beautifyCrabStatus( self, auto=False ):
        print self.logFileDir
        if self.details["status"] == "COMPLETED":
            print "{}COMPLETED!{} Suggest:".format(colors.GREEN,colors.NORMAL)
            print self.getMergeCommand()
            doneDir = self.logFileDir.replace("/crab_","/.{}_crab_".format(self.time))
            print "mv {} {}".format( self.logFileDir, doneDir)
            if auto:
                print "Actually to this stuff"
                mergeTier2Files.mergeTier2Files( self.getOutFileName(), self.getSrmPathFull() )
                os.rename(self.logFileDir, doneDir)

        else:
            print self.details["status"]
            self.jobSummary()



