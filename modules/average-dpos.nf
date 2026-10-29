process average_dpos {
    tag "$label"

    input:
    path main_averaging_file
    tuple val(label), path(csvs)

    output:
    tuple val("average-${label}"), path("rusty-metal-${label}-average.csv"), emit: output

    script:
    """
    python3 ${main_averaging_file} -i ${csvs} -o rusty-metal-${label}-average.csv
    """
}