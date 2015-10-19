#!/usr/bin/env python2
import sys

runD_firstRunNumber=256630

def createRunDjson(originalFileName):
    with open(originalFileName) as forig:
        jsonContent=forig.read()
        jsonContent=jsonContent[1:-1] # remove {}
        # remove all newlines and spaces
        jsonContent=jsonContent.replace("\n","")
        jsonContent=jsonContent.replace(" ","")
        # build a list with one element for each run number
        runNumberLines=[]
        for rnl in jsonContent.split(',"'):
            runNumberLines.append(rnl)
        # first one still starts with a "
        runNumberLines[0]=runNumberLines[0][1:]

        # find selected lines
        selLines=[]
        for rnl in runNumberLines:
            # print rnl
            rn=int(rnl.split('"')[0])
            if rn >= runD_firstRunNumber:
                selLines.append('"'+rnl)

        # write selection to a files
        outFileName=originalFileName.split("/")[-1].split(".")[0]
        outFileName+="_runD_only.txt"
        fsel = open(outFileName,'w')
        fsel.write('{\n')
        fsel.write(",\n".join(selLines))
        fsel.write('\n}\n')
        fsel.close()

        return outFileName

if __name__ == '__main__':
    originalFileName=sys.argv[1]
    selctedFile=createRunDjson(originalFileName)

