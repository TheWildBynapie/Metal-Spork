import csv
import re
from pathlib import Path

# Hardcode your result directories here
DIRECTORIES = [
    # #Blast data
    # "saved-results/blast data/MSA_graphs_by_taxa/corglcox1_PID50to70_67.69",
    # "saved-results/blast data/MSA_graphs_by_taxa/corglcox1_PID50to70_67.69",
    # "saved-results/blast data/MSA_graphs_by_taxa/corglcox1_PID60to80_67.62",
    # "saved-results/blast data/MSA_graphs_by_taxa/corglcox1_PID70to90_73.77",
    # "saved-results/blast data/MSA_graphs_by_taxa/humancox1_PID40to60_39.31",
    # "saved-results/blast data/MSA_graphs_by_taxa/humancox1_PID50to70_45.92",
    # "saved-results/blast data/MSA_graphs_by_taxa/humancox1_PID70to90_61.15",
    # "saved-results/blast data/MSA_graphs_by_taxa/humancox1_PID60to80_57.15",
    # "saved-results/blast data/MSA_graphs_by_taxa/humancox1_PID80to100_63.69",
    # "saved-results/blast data/MSA_graphs_by_taxa/lampreycox1_PID50to70_52.46",
    # "saved-results/blast data/MSA_graphs_by_taxa/lampreycox1_PID40to60_40.00",
    # "saved-results/blast data/MSA_graphs_by_taxa/lampreycox1_PID60to80_60.23",
    # "saved-results/blast data/MSA_graphs_by_taxa/lampreycox1_PID70to90_65.92",
    # "saved-results/blast data/MSA_graphs_by_taxa/lampreycox1_PID80to100_68.15",
    # "saved-results/blast data/MSA_graphs_by_taxa/octopuscox1_PID60to80_76.15",
    # "saved-results/blast data/MSA_graphs_by_taxa/octopuscox1_PID70to90_80.00",
    # "saved-results/blast data/MSA_graphs_by_taxa/octopuscox1_PID80to100_81.92",
    # "saved-results/blast data/MSA_graphs_by_taxa/ricecox1_PID60to80_67.92",
    # "saved-results/blast data/MSA_graphs_by_taxa/ricecox1_PID70to90_70.92",
    # "saved-results/blast data/MSA_graphs_by_taxa/ricecox1_PID80to100_76.77",
    
    # #NCBI data
    # "MSA-comparison-pipeline/saved-results/ncbi original data/MSA_graphs_by_taxa/mammalMHConly_52.79",
    # "saved-results/ncbi original data/MSA_graphs_by_taxa/mammalGrowthHormone_30.50",
    # "saved-results/ncbi original data/MSA_graphs_by_taxa/mammalFullHistoneH3only_94.00",
    # "saved-results/ncbi original data/MSA_graphs_by_taxa/eukaP53_36.21",
    # "saved-results/ncbi original data/MSA_graphs_by_taxa/eukaHistoneH4_55.86",
    # "saved-results/ncbi original data/MSA_graphs_by_taxa/bacteriaRpoB_54.43",
    # "saved-results/ncbi original data/MSA_graphs_by_taxa/bacteriaBetaLactamase_17.00",
    # "saved-results/ncbi original data/MSA_graphs_by_taxa/animalHistoneH3_81.71",
    # "saved-results/ncbi original data/MSA_graphs_by_taxa/animalCytochrome_32.14"
    # add more paths here
    
    #BAliBASE data
    # "results/MSA_graphs/BBA0001_24.64",
    # "results/MSA_graphs/BBA0002_46.38",
    # "results/MSA_graphs/BBA0003_41.62",
    # "results/MSA_graphs/BBA0005_53.15",
    # "results/MSA_graphs/BBA0006_32.54",
    # "results/MSA_graphs/BBA0007_40.08",
    # "results/MSA_graphs/BBA0009_55.92",
    # "results/MSA_graphs/BBA0008_49.54",
    # "results/MSA_graphs/BBA0010_30.69",
    # "results/MSA_graphs/BBA0011_52.93",
    # "results/MSA_graphs/BBA0013_52.00",
    # "results/MSA_graphs/BBA0012_44.00",
    # "results/MSA_graphs/BBA0014_39.14",
    # "results/MSA_graphs/BBA0015_31.93",
    # "results/MSA_graphs/BBA0016_43.00",
    # "results/MSA_graphs/BBA0017_43.07",
    # "results/MSA_graphs/BBA0018_32.93",
    # "results/MSA_graphs/BBA0019_48.71",
    # "results/MSA_graphs/BBA0020_38.86",
    # "results/MSA_graphs/BBA0021_38.79",
    # "results/MSA_graphs/BBA0022_55.50",
    # "results/MSA_graphs/BBA0024_33.79",
    # "results/MSA_graphs/BBA0025_36.57",
    # "results/MSA_graphs/BBA0026_29.14",
    # "results/MSA_graphs/BBA0027_30.29",
    # "results/MSA_graphs/BBA0028_62.07",
    # "results/MSA_graphs/BBA0029_55.14",
    # "results/MSA_graphs/BBA0030_47.36",
    # "results/MSA_graphs/BBA0031_34.29",
    # "results/MSA_graphs/BBA0032_59.64",
    # "results/MSA_graphs/BBA0033_33.57"
    
    #Alisim data
    "saved-results/alisim/MSA_graphs/sc0_1se40_89.14",
    "saved-results/alisim/MSA_graphs/sc0_1se41_87.64",
    "saved-results/alisim/MSA_graphs/sc0_1se42_82.14",
    "saved-results/alisim/MSA_graphs/sc0_5se40_64.29",
    "saved-results/alisim/MSA_graphs/sc0_5se41_61.71",
    "saved-results/alisim/MSA_graphs/sc0_5se42_61.36",
    "saved-results/alisim/MSA_graphs/sc1se40_47.64",
    "saved-results/alisim/MSA_graphs/sc1se41_43.57",
    "saved-results/alisim/MSA_graphs/sc1se42_40.93",
    "saved-results/alisim/MSA_graphs/sc2se40_25.79",
    "saved-results/alisim/MSA_graphs/sc2se41_22.21",
    "saved-results/alisim/MSA_graphs/sc2se42_23.14",
    "saved-results/alisim/MSA_graphs/sc4se40_11.79",
    "saved-results/alisim/MSA_graphs/sc4se41_10.07",
    "saved-results/alisim/MSA_graphs/sc4se42_10.57",
    "saved-results/alisim/MSA_graphs/sc6se40_7.50", 
    "saved-results/alisim/MSA_graphs/sc6se41_7.00", 
    "saved-results/alisim/MSA_graphs/sc6se42_7.07", 
    # "saved-results/alisim/MSA_graphs/sc10se40_5.29",
    # "saved-results/alisim/MSA_graphs/sc10se41_5.57",
    # "saved-results/alisim/MSA_graphs/sc10se42_5.57",
    # "saved-results/alisim/MSA_graphs/sc20se40_4.29",
    # "saved-results/alisim/MSA_graphs/sc20se41_4.71",
    # "saved-results/alisim/MSA_graphs/sc20se42_4.29",
    # "saved-results/alisim/MSA_graphs/sc40se40_4.14",
    # "saved-results/alisim/MSA_graphs/sc40se41_4.57",
    # "saved-results/alisim/MSA_graphs/sc40se42_4.36",
    # "saved-results/alisim/MSA_graphs/sc80se41_4.29"
    
    "saved-results/alisim/MSA_graphs/sc0_3se41_72.23",
    "saved-results/alisim/MSA_graphs/sc0_3se40_74.08",
    "saved-results/alisim/MSA_graphs/sc0_3se42_70.92",
    "saved-results/alisim/MSA_graphs/sc0_75se40_53.69",
    "saved-results/alisim/MSA_graphs/sc0_75se41_50.54",
    "saved-results/alisim/MSA_graphs/sc0_75se42_48.69",
    "saved-results/alisim/MSA_graphs/sc1_5se40_32.92",
    "saved-results/alisim/MSA_graphs/sc1_5se41_27.38",
    "saved-results/alisim/MSA_graphs/sc1_5se42_31.00",
    "saved-results/alisim/MSA_graphs/sc3se40_16.23",
    "saved-results/alisim/MSA_graphs/sc3se41_13.85",
    "saved-results/alisim/MSA_graphs/sc3se42_15.08"
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
