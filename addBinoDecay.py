#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys

gravitinoMass=1.0
chi01_decayWidth=1.0

# PDG14
sw2=0.231265 # sin²(theta_W)
cw2=1-sw2
mZ=91.1876

def outputformat(number):
    return ("%.8e"%number).upper()

def BRg(m):
    if (m<mZ) return 1
    return cw2/(cw2+sw2*(1.-mZ**2/m**2)**4)
def BRZ(m):
    if (m<mZ) return 0
    return sw2*(1.-mZ**2/m**2)**4/(cw2+sw2*(1.-mZ**2/m**2)**4)

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print "specify SLHA file as input parameter"
        exit(0)

    finname=sys.argv[1]
    foutname=finname.split('.slha')[0]+"_chi01decays.slha"
    print "reading from",finname
    print "writing to",foutname
    print

    chi01Mass=None
    with open(finname,'r') as fin, open(foutname,'w') as fout:
        currentBlock=None
        for line in fin:
            if "BLOCK" in line:
                currentBlock=line.split()[1]
            elif currentBlock=="MASS":
                mass=line.split()
                if mass[0]=="1000022":
                    chi01Mass=float(mass[1])
                    print "found chi01 mass:",chi01Mass
                if mass[0]=='#' and len(mass)==1: # end of mass block (depends on the comment line!!)
                    write="   1000039     %s   # ~G\n"%outputformat(gravitinoMass)
                    fout.write(write)
                    print "written",write

            fout.write(line)
        print "writing chi01 decay block"
        dec="#\n#         PDG            Width\n"
        dec+="DECAY   1000022     %s   # neutralino1 decays\n"%outputformat(chi01_decayWidth)
        dec+="#          BR         NDA      ID1       ID2\n"
        dec+="     %s    2     1000039        22   # BR(~chi_10 -> ~G gamma)\n"%outputformat(BRg(chi01Mass))
        dec+="     %s    2     1000039        23   # BR(~chi_10 -> ~G Z    )"%outputformat(BRZ(chi01Mass))
        print dec
        fout.write(dec)
