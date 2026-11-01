process average_dpos {
    tag "$label"

    input:
    path main_averaging_file
    tuple val(label), path(csvs), val(identity)

    output:
    tuple val("average-${label}_${identity}"), path("rusty-metal-${label}-average_${identity}.csv"), val(identity), emit: output

    script:
    """
    python3 ${main_averaging_file} -i ${csvs} -o rusty-metal-${label}-average_${identity}.csv
    """
}