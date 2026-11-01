process rustyMetal {
    tag "${sample_id}"

    input:
    tuple val(sample_id), path(alignments), val(identity)

    output:
    tuple val(sample_id), path("rusty_metal_${sample_id}.csv"), val(identity), emit: output

    script:
    """
    rusty-metal ${alignments.join(' ')} -o rusty_metal_${sample_id}.csv
    """
}