import csv
import re
from pathlib import Path

# Hardcode your result directories here
DIRECTORIES = [
    #Blast data
    "saved-results/blast data/MSA_graphs_by_taxa/corglcox1_PID50to70_67.69",
    "saved-results/blast data/MSA_graphs_by_taxa/corglcox1_PID50to70_67.69",
    "saved-results/blast data/MSA_graphs_by_taxa/corglcox1_PID60to80_67.62",
    "saved-results/blast data/MSA_graphs_by_taxa/corglcox1_PID70to90_73.77",
    "saved-results/blast data/MSA_graphs_by_taxa/humancox1_PID40to60_39.31",
    "saved-results/blast data/MSA_graphs_by_taxa/humancox1_PID50to70_45.92",
    "saved-results/blast data/MSA_graphs_by_taxa/humancox1_PID70to90_61.15",
    "saved-results/blast data/MSA_graphs_by_taxa/humancox1_PID60to80_57.15",
    "saved-results/blast data/MSA_graphs_by_taxa/humancox1_PID80to100_63.69",
    "saved-results/blast data/MSA_graphs_by_taxa/lampreycox1_PID50to70_52.46",
    "saved-results/blast data/MSA_graphs_by_taxa/lampreycox1_PID40to60_40.00",
    "saved-results/blast data/MSA_graphs_by_taxa/lampreycox1_PID60to80_60.23",
    "saved-results/blast data/MSA_graphs_by_taxa/lampreycox1_PID70to90_65.92",
    "saved-results/blast data/MSA_graphs_by_taxa/lampreycox1_PID80to100_68.15",
    "saved-results/blast data/MSA_graphs_by_taxa/octopuscox1_PID60to80_76.15",
    "saved-results/blast data/MSA_graphs_by_taxa/octopuscox1_PID70to90_80.00",
    "saved-results/blast data/MSA_graphs_by_taxa/octopuscox1_PID80to100_81.92",
    "saved-results/blast data/MSA_graphs_by_taxa/ricecox1_PID60to80_67.92",
    "saved-results/blast data/MSA_graphs_by_taxa/ricecox1_PID70to90_70.92",
    "saved-results/blast data/MSA_graphs_by_taxa/ricecox1_PID80to100_76.77",
    
    #NCBI data
    "MSA-comparison-pipeline/saved-results/ncbi original data/MSA_graphs_by_taxa/mammalMHConly_52.79",
    "saved-results/ncbi original data/MSA_graphs_by_taxa/mammalGrowthHormone_30.50",
    "saved-results/ncbi original data/MSA_graphs_by_taxa/mammalFullHistoneH3only_94.00",
    "saved-results/ncbi original data/MSA_graphs_by_taxa/eukaP53_36.21",
    "saved-results/ncbi original data/MSA_graphs_by_taxa/eukaHistoneH4_55.86",
    "saved-results/ncbi original data/MSA_graphs_by_taxa/bacteriaRpoB_54.43",
    "saved-results/ncbi original data/MSA_graphs_by_taxa/bacteriaBetaLactamase_17.00",
    "saved-results/ncbi original data/MSA_graphs_by_taxa/animalHistoneH3_81.71",
    "saved-results/ncbi original data/MSA_graphs_by_taxa/animalCytochrome_32.14"
    # add more paths here
]

OUTPUT_CSV = "identity_vs_dpos.csv"


def parse_dir_name(dir_path):
    """Split a directory name like 'corglcox1_PID50to70_67.69' into
    (metadata='corglcox1_PID50to70', percent_identity=67.69)."""
    name = Path(dir_path).name
    metadata, _, pid_str = name.rpartition('_')
    try:
        percent_identity = float(pid_str)
    except ValueError:
        return None, None
    return metadata, percent_identity


def extract_average_dpos(summary_file):
    text = Path(summary_file).read_text()
    match = re.search(r"Average dPos:\s*([\d.]+)", text)
    if not match:
        return None
    return float(match.group(1))


def main():
    rows = []
    for dir_path in DIRECTORIES:
        metadata, percent_identity = parse_dir_name(dir_path)
        if metadata is None:
            print(f"WARNING: couldn't parse percent identity from '{dir_path}', skipping")
            continue

        summary_file = Path(dir_path) / "MSA_summary.txt"
        if not summary_file.exists():
            print(f"WARNING: no MSA_summary.txt found in '{dir_path}', skipping")
            continue

        average_dpos = extract_average_dpos(summary_file)
        if average_dpos is None:
            print(f"WARNING: couldn't find 'Average dPos' in '{summary_file}', skipping")
            continue

        rows.append((percent_identity, average_dpos, metadata))

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["percent_identity", "average_dpos", "metadata"])
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
