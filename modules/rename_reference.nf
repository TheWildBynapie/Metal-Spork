process rename_reference {
    tag "$sample_id"

    input:
    tuple val(sample_id), path(reference)

    output:
    tuple val(sample_id), path("reference.*")

    script:
    def ext = reference.extension ? ".${reference.extension}" : ""
    """
    ln -s ${reference} reference${ext}
    """
}