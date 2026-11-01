process alistat_identity {
    tag "${sample_id}"

    input:
    tuple val(sample_id), path(aln)

    output:
    tuple val(sample_id), stdout

    script:
    """
    esl-alistat ${aln} | grep "Average identity:" | grep -oE '[0-9]+(\\.[0-9]+)?'
    """
}

process average_identity {
    tag "$sample_id"

    input:
    tuple val(sample_id), val(identities)

    output:
    tuple val(sample_id), stdout, emit: output

    script:
    def values = identities.join(' ')
    """
    echo "${values}" | awk '{
        sum = 0
        for (i = 1; i <= NF; i++) sum += \$i
        printf "%.2f", sum/NF
    }'
    """
}