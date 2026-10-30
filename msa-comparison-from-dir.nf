#!/usr/bin/env nextflow
include { rustyMetal } from './modules/rusty-metal.nf'
include { average_dpos } from './modules/average-dpos.nf'
include { graphs } from './modules/graphing.nf'
include { alistat_identity; average_identity } from './modules/alistat.nf'

/*
* Takes directories of ALREADY-ALIGNED .fasta MSAs and runs them straight
* into comparison/summary steps, skipping the align process entirely.
* Each directory = one comparison group. Its basename becomes the sample_id.
* Each file inside it (minus .fasta) becomes that alignment's run_id label.
*/
params {
    msaDirs: List<String> = ['testdata/existing_msas']
    resultsDir: String = 'results'
}

workflow {
    main:

    // Flatten every directory into (sample_id, run_id, path) triples -- one per MSA file
    msa_ch = channel.fromList(params.msaDirs)
    .flatMap { dirPath ->
        def sampleId = file(dirPath).name
        def matchingFiles = files("${dirPath}/*.fasta")
        // file() with a glob returns a single Path if there's only one match, or a List otherwise -- normalize both cases
        matchingFiles = matchingFiles instanceof List ? matchingFiles : [matchingFiles]
        matchingFiles.collect { f -> tuple(sampleId, f) } //f.name.replaceAll(/\.fasta$/, ''),
    }

    //msa_ch.view { entry -> "MSA entry: ${entry}" }

    //Regroup by sample_id, same shape rustyMetal already expects
    alignments_by_sample = msa_ch.groupTuple()

    rustyMetal(alignments_by_sample)

    //%identity per alignment, averaged per sample -- same as before
    alistat_identity(msa_ch)
    identity_by_sample = alistat_identity.out
        .map { sample_id, identity -> tuple(sample_id, identity.trim()) }
        .groupTuple()
    average_identity(identity_by_sample)

    // Collect every replicate's CSV into one list for averaging
    replicate_csvs = rustyMetal.out.output
        .map { _sample_id, csv -> csv }
        .collect()
        .map { csvs -> tuple("total-${workflow.profile}", csvs) }

    average_dpos(file('non-nextflow/average_dpos.py'), replicate_csvs)

    all_for_graphing = rustyMetal.out.output.mix(average_dpos.out.output)

    graphs(file('non-nextflow/make_distance_matrix.py'), all_for_graphing)

    publish:
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