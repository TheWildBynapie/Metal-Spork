# MSA tool details

### What MSA tools can I use with Metal Spork?

In my thesis I used a specific selection of MSA tools and versions. These are listed below.

Annoyingly, not any aligner can just be slotted in without editing the code. If you wish to use any MSA tools not included in the list below, edit your copy of
[`modules/aligners.nf`](../modules/aligners.nf)

# Aligner details
| Name          | Version number | Latest version as of | original release date (1.0) | Latest major version release date (X.0) | Notes |
| ------------- | -------------- | ------------------------- | ---- | ---- | ----- |
| AMAP-align    |AMAP.2.2|30/08/2026| 2008 | 2014 | |
| Bali-Phy      | 4.3 | | 2006 | 2025 | |
| Clustal Omega |1.0.3|not latest| 2011 | 2011 | clustal.org hates me (I'm blocked and can't download a newer version)|
| ClustalW      |2.1|30/08/2026| 1994 | 2007 | at least this is latest anyway lol|
| FAMSA2        |     |  | 2026 | 2026 | |
| FSA           |1.15.9|11/09/2026| 2009 | 2009 |       |
| Kalign        |3.4.0| not latest| 2005 | 2019 | I should've got 3.5.1. Sorry I didn't |
| MAFFT         |v7.526|30/08/2026| 2002 | 2013 | |
| MUSCLE        |3.8| | 2004 | 2004 | |
| Muscle5       |5.3.linux64|30/08/2026| 2021 | 2021 | |
| PRANK         |v.250331|                           | 2005 | 2017* |
| ProbCons      |1.12|30/08/2026| 2005 | 2005 |  |
| T-Coffee      |Version_13.46.0.919e8c6b| | 2000 | 2018 | |

### Abandoned aligners
| Name          | Notes |
| ------------- | --------------------- |
| Any structural aligner | those take .pdb input instead of .fasta |
| UPP2 | I could not install it despite trying for 2 hours. Those people really need to improve their software. |
| MLProbs | same as UPP2. Genuinely disgusting handling of software, the readmes are so bad |
| UPP | requires an older version of python that seems to be incompatible with its own dependencies... fascinating software :((( (Needs <=3.10 and pasta needs 3.13) |
