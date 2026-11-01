# Metal Spork
A Nextflow 26.04 pipeline to compare MSAs made by different MSA tools using dpos from Blackburn and Whelan (2012), and automated visualisation.

## Documentation

Start here, then open the focused document for what you are interested in.

| Document | Purpose |
| --- | --- |
| [`docs/Workflow.md`](docs/Workflow.md) | Explanation of the inputs, and outputs of the pipeline, and summary of the steps in the workflow |
| [`docs/Download.md`](docs/Download.md) | New contributor setup and first local run |
| [`docs/ActualMethods.md`](docs/ActualMethods.md) | User guide style version of my thesis methods, including specific commands and such to reproduce my results |
| [`docs/MSAtoolsDetails.md`](docs/MSAtoolsDetails.md) | List of supported MSA tools, the versions I used in my thesis, and how to add support for additional MSA tools |
| [`docs/UnfinishedResults.md`](docs/UnfinishedResults.md) | Info about analyses that I started trying to do but never finished before writing the thesis.  |

## Setup overview

1. Prerequisite packages
   * Nextflow 26.04 (or later I assume, but untested)
   * Python 3.14
     - pandas
     - Biopython
     - Matplotlib
     - NumPy
     - scikit-learn
     - SciPy
   * Bash
   * rusty-MetAl

2. MSA tools
   * Any MSA tool you use will need to be installed locally.
   * The list of ones I used in my thesis is in [`docs/MSAtoolsDetails.md`](docs/MSAtoolsDetails.md).

3. Clone the repo
```bash
git clone https://github.com/TheWildBynapie/Metal-Spork
```

4. Then you should be ready to go!
This should do a small test run on a tiny fake dataset in [`testdata/`](testdata/).
```bash
nextflow msa-comparison.nf 
```

5. You can use [`removeClutter.sh`](removeClutter.sh) to clear the results, and work directories, and the nextflow logs.
```bash
./removeClutter.sh
```
a tip is to do './rem' and hit tab to autocomplete it

## Basic usage

The parameters for the pipeline are lists, and currently do not support pure CLI input. I used the nextflow.config file throughout my data processing. I include instructions for using it in [`docs/Workflow.md`](docs/Workflow.md) but you can also use a parameter file as follows:
```JSON
{
  "inputs": [
    "testdata/test.fasta",
    "testdata/test_gapless.fasta:testdata/test_reference.fasta"
  ]
}
```
Then specify the parameter file
```bash
nextflow run msa-comparison.nf -params-file params.json
```

   
