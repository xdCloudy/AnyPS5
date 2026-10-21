# libSceVrTracker technical debt

### Unknown function info

- [sceVrTrackerCpuProcess, sceVrTrackerGetResult, sceVrTrackerGetTime, sceVrTrackerGpuSubmit, sceVrTrackerGpuWait and sceVrTrackerInit](../../../core/libs/prx/libSceVrTracker/Export.cpp) (libSceVrTracker) - names and NIDs are present in the [PS5 3.20 export inventory](https://github.com/DNNDHH/PS5-3.20_Libs/blob/b2a77c09cd71c01f34c790cfbe98c751a13262ad/libSceVrTracker.c), but no credible prototypes were found. The declarations have no parameters solely to resolve known imports; this is not an ABI claim and callers must not call them until signatures are verified

- [libSceVrTracker pending exports](../../../core/libs/prx/libSceVrTracker/Export.cpp) - 24 named callable exports are listed in the [PS5 3.20 export table](https://github.com/DNNDHH/PS5-3.20_Libs/blob/b2a77c09cd71c01f34c790cfbe98c751a13262ad/libSceVrTracker.c) and were cross-checked against the same module in PS5 firmware 13.60. Their signatures and behaviour are unverified; the declarations use the no-parameter unknown-signature convention and throw through `NotImplemented_nid_no_patch`.
