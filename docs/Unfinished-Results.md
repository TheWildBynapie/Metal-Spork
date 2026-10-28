# Unfinished results

This includes analyses that did not get included in the thesis because they were scrapped as a result of time constraints.

## Ensembles of individual tools with parameter perturbations 

Most tools do not have parameters that result in significant changes  

## Ensembles on BaliBASE data 

Differences between tools are smaller on BaliBASE data for the same PID ranges. This is potentially concerning as this is also simply data of real proteins, yet the behaviour of MSA tools is different with BaliBASE datasets, which allow tools to optimize on them, compared to random real data from other sources.  
The clusters of algorithms do not change between BaliBASE and other data, which is good. Arguably, they are more consistent within BaliBASE datasets than other data.  
When using the provided reference alignments, ClustalO is most often the closest followed by MAFFT or Kalign, which is consistent with the same group from the typical clusters. Since dpos compares whole alignments the parts of the reference alignment not included in BaliBASE’s own scoring strategy do get included for this, which makes dpos used on the reference alignment a little worse. 
