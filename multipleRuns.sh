#!/bin/bash
#./multipleRuns.sh

#Typical pipeline runs
#nextflow msa-comparison.nf -profile blasthuman
#nextflow msa-comparison.nf -profile blastlamprey
#nextflow msa-comparison.nf -profile blastoctopus
#nextflow msa-comparison.nf -profile blastrice
#nextflow msa-comparison.nf -profile blastcorgl

#Premade MSA runs

##blast runs
###by PID
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile pid39to50
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile pid50to60
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile pid60to70
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile pid70to82
###by taxa
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile human
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile lamprey
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile octopus
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile rice
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile corgl

##ncbi runs
###by taxa
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile ncbimammal
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile ncbianimal
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile ncbieuka
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile ncbibacteria
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile ncbivirus

# ##by PID
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile ncbipid0to20
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile ncbipid20to40
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile ncbipid40to60
# nextflow msa-comparison-from-dir.nf -c fromdir.config -profile ncbipid80to100

# Runs for internal tool comparisons:
##mafft
#nextflow msa-comparison.nf -profile blasthuman,mafft
#nextflow msa-comparison.nf -profile blastlamprey,mafft

##clustalo
#nextflow msa-comparison.nf -profile blasthuman,clustalo
#nextflow msa-comparison.nf -profile blastlamprey,clustalo

##clustalo
#nextflow msa-comparison.nf -profile blasthuman,muscle
#nextflow msa-comparison.nf -profile blastlamprey,muscle