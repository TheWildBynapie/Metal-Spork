# Methods

This doc is a copy of the methods section of the thesis, but in a user-guide style, so that exact commands and file movements can be replicated more easily, given someone wanted to repeat the analysis on my data, or extract data in the same way and rerun an analysis on it.
There are 2 Major sections, with subsections:
* Data collection (How I downloaded data. How I preprocessed and processed it is later)
  - NCBI data
  - Blast data
* How the workflow works, and how it is used on my data
  - Main workflow
  - Helper code for data extraction
  - How I used the workflow on my data (preprocessing and processing)

# Data  

## NCBI data 

Protein sequences were retrieved from NCBI protein, using searches of the following format:  

    histone h3[All Fields] AND "Mammalia"[Organism]

If the dataset would be too large, refseq only, and failing that – swiss-prot only – would be retrieved from the results. 
FASTA format of the search results were taken for a somewhat conserved, and somewhat badly conserved gene for each group.  

    Mammals: Histone H3, major histocompatibility complex, and growth hormone. 

    Animals: Histone H3, and cytochrome c oxidase subunit 1.  

    Eukaryotes: Histone H4, and p53.  MSA-comparison-pipeline

    Bacteria: RpoB, and Beta lactamase.  

    Viruses: RdRp, HIV env, and Influenza Hemagglutinin.  

## Blastp 

For each of mammals, chordates, animals, eukaryotes, and bacteria a swiss-prot sequence was selected from UniProtKB for cox1. Chosen sequences were relatively far away from humans on the tree of life within each group and then used each as a blast query sequence. Blastp was used with the clusteredNR database, and maximum 5000 matches in algorithm parameters. Otherwise default parameters as of 10/10/2026. Accession and organism scopes were: 

    P00395 (human cox1), mammalia 

    Q35536 (lamprey cox1), chordates 

    Q9G6J1 (octopus cox1), animals 

    P14578 (rice cox1), eukaryotes 

    Q79VD7 (corynebacterium glutamicum cox1), bacteria 

    Q20NV3 (Influenza A virus (I80AD on UniProtKB)), viruses 

Both the unaligned FASTA sequences and the CSV hit table were downloaded and later pre-processed using the processes described below. 

# Nextflow workflow 

### How dpos is calculated 

I used an implementation of MetAL for only dpos, where dpos  (Blackburne & Whelan, 2012)  is calculated for the whole of each alignment pair. It is calculated for all pairs of MSAs created within the ensemble. It is a number that ranges between 0 and 1, where 0 represents identical MSAs, and 1 is completely different. It uses homology sets to calculate the difference between each MSA for each residue in each sequence of the MSAs. A homology set is all the other residues in the column of the alignment beside the residue we’re looking at. Importantly, gaps are labeled as Gx where x is the position of the residue/nucleotide to the left in the unaligned sequence. Therefore, G1 and G2 are considered different. dpos uses this formula: 

Intuitively, dpos looks at each residue and asks: was this residue aligned to the exact same set of residues and gaps in the other MSA or not? 

How my tool works 

## Primary pipeline 

msa-comparison.nf is the main workflow file for this pipeline. It creates ensembles of MSAs, calculates dPos using rusty-metal, and then visualizes the distances between all the MSAs in the ensemble using multi-dimensional scaling (MDS), and hierarchical clustering. It also produces some summary data as well. 

As input, it requires a list of alignment tools, and a list of .fasta files or a directory of .fasta files. If using a directory, the file extensions must be exactly “.fasta”. When listing single files, you may optionally provide a reference alignment file which is included in the ensemble all-against-all comparison. 

The format of each parameter is given below: 

params.inputs = ['path/to/unaligned.fasta:path/to/reference.fasta', ‘path/to/unaligned.fasta’, ‘path/to/directoryOfUnalignedFastas/’,] 

params.runs = ['runid:tool:options',] 

Since each tool has different input parameters, the requirements and possiblities for ‘options’ must be checked per aligner. This is listed in GitHub. 

The pipeline outputs 3 directories: MSA_graphs, MSA_outputs, and rusty-metal. MSA_outputs contains all the MSAs in .fasta format. Each input file has a corresponding directory with its MSA ensemble. Rusty-metal contains csv files with the raw dPos measurements. Each ensemble has 1 corresponding file, which contains dPos for all pairs of aligners in that ensemble.  

MSA_graphs has 1 directory per ensemble, plus 1 extra which uses averages over all ensembles in the workflow. Each contains 5 files.  

    MSA_distances_nolines.png is an MDS showing MSAs in a euclidean space. 

    MSA_distances.png is the same, but each MSA has distances to its 3 closest other MSAs shown. MDS cannot express all distances perfectly in a 2D space, hence these lines show actual dPos distances, not the visually apparent distances. MDS provides a ‘stress’ value which is a measure of how badly the distances fit into the space. Low is good.  

    MDS stress is stored in MSA_summary.txt. That also contains the average dPos value for the ensemble, and the sum of dPos values for all MSA tools. Thus, if you wish to use this to select MSAs from the ensemble you can pick the lowest one. This is not recommended, as far better post-processing tools exist.  

    MSA_hierarchical is easiest to interpret. It attempts to show MSAs in a tree structure but is less detailed than the MDS output. One can look for consistent patterns in tree structure across different data.  

    Finally, average_identity.txt contains the average percent identity (PID) between the sequences in the unaligned file. This is calculated using esl-alistat on all MSAs in the ensemble and averaging those. 

## Helper code 

msa-comparison-from-dir.nf does the same thing, except it accepts a directory of premade MSAs. This allows you to create MSAs once and regroup them to form different average results. 

data-acquisition.nf uses seqkit grep and seqtk to sample only fasta entries that contain a given name, and then subsamples 50, or a number of your choice sequences from that dataset. For example: only take entries with ‘Cytochrome c oxidase subunit 1’ in the header and then subsample 50 of those. This allows you to do this on several data files at once. 

dataac-blast.nf does the same but additionally preprocesses each .fasta file given using their corresponding blast hit csv table to extract specific %identity ranges and require a minimum coverage of the query sequence. This %identity is between the query sequence and all others, rather than the total %identity that esl-alistat calculates, so it is a proxy. 

multipleRuns.sh is a helpful script for running the pipeline locally. I use it to run several msa-comparison.nf calls so it creates averages of different groups, localizes failed runs, so I don’t need to rerun a single massive workflow if it fails, and prevents nexflow using too much processing power which often caused crashes. Given an HPC and code edits all these could be fixed, but there was insufficient time to containerize the pipeline.  

append_identity_to_names.py is a python script which uses the esl-alistat results within a results/ directory of msa-comparison.nf or msa-comparison-from-dir.nf, to rename files with the PID of the corresponding unaligned sequences file. This makes grouping data by PID easier. 

## How I used it 

### Blast data 

Once I had the BLAST data, I used dataac-blast.nf to filter, subsample it, and split it into PID ranges. This is the command used: 

nextflow dataac-blast.nf -c dataac-blast.config 

The file dataac-blast.config is in GitHub. Then I renamed the files to be simpler by switching to the directory and using: 

PERL5LIB= rename 's/blastp5000[^_]*//; s/_50seq//' * 

Afterwards, I sorted the files by taxa into profiles in nextflow.config to use with msa-comparison.nf: human, lamprey, octopus, rice, corgl. I then used multipleRuns.sh to run msa-comparison.nf on each group: 

nextflow msa-comparison.nf -profile human 
nextflow msa-comparison.nf -profile lamprey 
nextflow msa-comparison.nf -profile octopus 
nextflow msa-comparison.nf -profile rice 
nextflow msa-comparison.nf -profile corgl 

After that I moved the results to a directory ‘saved-results/blast data/’, changed to that directory and used the python script append_identity_to_names.py: 

python3 append_identity_to_names.py . 

Now it is easy to see PID of datasets. I created profiles for msa-comparison-from-dir.nf with these bins: 39-50, 50-60, 60-70, 70-82. Then I ran multipleRuns.sh for this as well: 

nextflow msa-comparison-from-dir.nf -c fromdir.config -profile pid39to50 
nextflow msa-comparison-from-dir.nf -c fromdir.config -profile pid50to60 
nextflow msa-comparison-from-dir.nf -c fromdir.config -profile pid60to70 
nextflow msa-comparison-from-dir.nf -c fromdir.config -profile pid70to82 

I took the directories for the new averaged graphs and discarded the rest as it is identitcal to the previous set of runs. 

### NCBI data 

I subsampled and filtered the data using data-acquisition.nf: 

nextflow data-acquisition.nf -c dataac.config 

Then I basically did the same procedure as above. Rename using the same command, create profiles by taxa, do multipleRuns.sh to get the averages of each, rename files with PID, sort by identity, make new config profiles, run multipleRuns.sh again. Detailed version in GitHub. 

### BAliBASE data 

It is important to note, that BAliBASE’s scoring strategy does not use the whole reference alignment, but rather analyses small highly reliable sections of it, and only uses tool performance on those pieces. This implementation of dpos calculates it between whole alignments and therefore includes typically unincluded parts of the BAliBASE reference when that is used.
