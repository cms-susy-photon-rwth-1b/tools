# tools
General tools for data manipulation, Job management, etc.

* `mergeTier2Files.py`:
usage `./mergeTier2Files.py <outputFile>.root <srm-source-path>`
- `<srm-source-path>` has to be of the form:
  "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/<...>/<date>_<time>/"
  the `<date>_<time>` directory contains numbered directries `0001`,`0002`,... that contain the root files
example usage:
```./mergeTier2Files.py out.root srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/jolange/data/Test/GJets_HT-400to600_Tune4C_13TeV-madgraph-tauola/sizeCheck/150504_120017/```
