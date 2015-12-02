# tools
General tools for data manipulation, Job management, etc.

## `mergeTier2Files.py` ##
usage `./mergeTier2Files.py <outputFile>.root <srm-source-path>`
- `<srm-source-path>` has to be of the form:
  "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/<...>/<date>_<time>/"
-  the `<date>_<time>` directory contains numbered directries `0001`,`0002`,... that contain the root files
- example usage:
```./mergeTier2Files.py out.root srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/jolange/data/Test/GJets_HT-400to600_Tune4C_13TeV-madgraph-tauola/sizeCheck/150504_120017/```

## `checkPrescale.py` ##
Use `./checkPrescale.py` to check if triggers have prescales for events in a file.
If a trigger has a prescale, the script prints `runNumber:luminosityBlockNumber:eventNumber` and the used prescale.
Change
- `myTriggers` the triggers you want to inspect
- `events` the file you want to check

## `runDlumi.py` ##
Calculate the lumi for 25ns data for runD (and possibly later) only for a given JSON file:

```
./runDlumi.py /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-258159_13TeV_PromptReco_Collisions15_25ns_JSON_v3.txt
```

Calls the `brilcalc` tool, which has to be [installed](http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html#installation).

## `showGenSUSYcontent.py` ##
Show PDG ID histograms in the relevant range for SUSY particles:

    ./showGenSUSYcontent.py file.root

If MINIAODSIM or AODSIM is contained in the filename, the right Trees and Branches are used. Otherwise, the 13 TeV and 8 TeV paths are tried.
## `addBinoDecay.py` ##
adds a Decay block (chi01->~G X) to a GGM SLHA file (neutralino1 is stable there, Pythia8 can no longer calculate the decay on its own)
for bino-like NLSP

    ./addBinoDecay.py M2_640_M1_630.slha

## `copy_cfg.py` ##
Copy a part of a file or dataset to a local file. The output filename will be guessed from the input file or dataset.

    cmsRun copy_cfg.py dataset=/SinglePhoton/Run2015D-PromptReco-v4/MINIAOD [maxEvents=50]
