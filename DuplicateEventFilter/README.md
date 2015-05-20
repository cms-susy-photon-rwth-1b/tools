Checks if a tree contains duplicate events.
Events are considered as duplicates if their runNumber,eventNumber and luminosityBlockNumber coincide.

usage:
```./DuplicateEventFilter.py file.root```

If this is used as a module, the function `filterFile(filename, treename)` can be used.
