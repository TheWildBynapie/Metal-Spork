#!/usr/bin/env nextflow
include { align } from './modules/aligners.nf'
include { rustyMetal } from './modules/rusty-metal.nf'
include { average_dpos } from './modules/average-dpos.nf'
include { graphs } from './modules/graphing.nf'
include { alistat_identity; average_identity } from './modules/alistat.nf'

/*
* Inputs: the .fasta files to be aligned, and have those alignments compared.
* Runs: the runs of the MSA tools to be executed per fasta file.*
*
* The parameter values here are examples. They are overridden by the config file.
*/
params {
    inputs: List<String> = ['testdata/test_gapless.fasta']
    resultsDir: String = 'results'
    runs: List<String> = [
        /*Each line defines a run of a MSA tool.
        * Run names are arbitrary, but must be unique. They are used in the output file names.
        * The format is:
        * '<run name>:<tool name>:<tool_options>'
        */
        'mafft_auto:mafft:mafft --auto', 
        'mafft_linsi:mafft:linsi',
        'muscle:muscle:-align', 
        'kalign:kalign:', 
        't_coffee:t_coffee:', 
        'probcons:probcons:', 
        'clustalw:clustalw:', 
        'clustalo:clustalo:', 
        'amap:amap:', 
        'prank:prank:', 
        'fsa:fsa:'
    ]
}

workflow {
    main:
    input_ch = channel.fromList(params.inputs)
        .flatMap { entry ->
            def parts = entry.split(':', 2)
            def inputPath = parts[0]
            def reference = parts.size() > 1 ? parts[1] : null
            def target = file(inputPath)

            if (target.isDirectory()) {
                if (reference != null) {
                    log.warn "Reference '${reference}' given alongside directory '${inputPath}' is ignored -- directory entries don't support a shared reference."
                }
                def group = target.name  // e.g. "human", "lamprey"
                def matches = files("${inputPath}/*.fasta")
                matches = matches instanceof List ? matches : [matches]
                matches.collect { f -> tuple(f.simpleName, f, null, group) }
            } else {
                [ tuple(target.simpleName, target, reference ? file(reference) : null, null) ]
            }
        }

    //Each run is a tuple of (run_id, tool, options)
    run_ch = channel.fromList(params.runs)
        .map { entry ->
           def (run_id, tool, options) = entry.split(':', 3)
           tuple(run_id, tool, options)
        }

    // cartesian product: every (run, sample_id / fasta) combination
    combos = run_ch.combine(input_ch)
        .map { run_id, tool, options, sample_id, fasta, _reference, _group -> tuple(run_id, tool, options, sample_id, fasta) }

    //Align everything
    align(combos)

    //Compute %identity for every alignment align produced, then average per sample
    alistat_identity(align.out.alignment)
    identity_by_sample = alistat_identity.out
        .map { sample_id, identity -> tuple(sample_id, identity.trim()) }
        .groupTuple()
    average_identity(identity_by_sample)

    //Build a (sample_id, 'reference', path) entry for every input that specified one
    reference_ch = input_ch
        .filter { _sample_id, _fasta, reference, _group -> reference != null }
        .map { sample_id, _fasta, reference, _group -> tuple(sample_id, reference) }

    //Regroup alignments by the fasta file/sample_id
    alignments_by_sample = align.out.alignment
        .mix(reference_ch)
        .groupTuple()          //(sample_id, [fasta1, fasta2, ..., fastaN])  -- one emission PER input file

    //Run rusty-metal, and then graphing on each group of alignments
    rustyMetal(alignments_by_sample)
    
        // Only samples that came from a directory have a group
    sample_to_group = input_ch
        .filter { _sample_id, _fasta, _reference, group -> group != null }
        .map { sample_id, _fasta, _reference, group -> tuple(sample_id, group) }

    // Per-directory CSV lists: (group, [csv1, csv2, ...])
    group_csvs = rustyMetal.out.output
        .join(sample_to_group)                       // (sample_id, csv, group) -- standalone files drop out here automatically
        .map { _sample_id, csv, group -> tuple(group, csv) }
        .groupTuple()

    // The existing "everything combined" total, reshaped to carry a label too
    total_csvs = rustyMetal.out.output
        .map { _sample_id, csv -> csv }
        .collect()
        .map { csvs -> tuple('total', csvs) }

    average_targets = group_csvs.mix(total_csvs)

    average_dpos(file('non-nextflow/average_dpos.py'), average_targets)

    // Mix the averaged result back into the same channel shape as individual runs
    all_for_graphing = rustyMetal.out.output.mix(average_dpos.out.output)

    graphs(file('non-nextflow/make_distance_matrix.py'), all_for_graphing)

    publish:
    aligners     = align.out.alignment
    rustyMetal   = rustyMetal.output
    MDS          = graphs.out.MDS
    MDS_nolines  = graphs.out.MDS_nolines
    hierarchical = graphs.out.hierarchical
    summary      = graphs.out.summary
    avgIdentity  = average_identity.out.output

    onComplete:
    if (workflow.success) {
        def cmd = "python3 ${projectDir}/non-nextflow/append_identity_to_names.py ${params.resultsDir}"
        cmd.execute().waitForProcessOutput(System.out, System.err)
    } else {
        log.warn "Skipping append_identity_to_names.py -- workflow did not complete successfully."
    }
}

output {
    aligners {
        path 'MSA_outputs'
    }

    rustyMetal {
        path 'rusty-metal'
    }

    MDS {
        path 'MSA_graphs'
    }
    MDS_nolines {
        path 'MSA_graphs'
    }
    hierarchical {
        path 'MSA_graphs'
    }
    summary {
        path 'MSA_graphs'
        mode 'copy'
    }
    avgIdentity {
        path 'MSA_graphs'
        mode 'copy'
    }
}
