import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
import pandas as pd
import argparse

#My modules
import mds, hierarchical_clustering

"""Writes the following to a text file:
    MDS stress value
    average dPos between all pairs of MSAs
    For each MSA tool, the sum of its dPos values to all other tools, sorted from smallest to largest
    - this essentially tells you 'which MSA is the most similar to all others'
    * The latter 2 details, are inspired by MUMSA (2005)
    """
def write_summary(D, points, stress, output_file):
    n = len(points)
    # Only count each pair once (upper triangle, excluding the zero diagonal)
    i_upper, j_upper = np.triu_indices(n, k=1)
    pairwise_dpos = D[i_upper, j_upper]
    avg_dpos = pairwise_dpos.mean()

    # Per-tool avg: sum of that tool's row (its distance to every other tool)
    tool_avgs = [(points[i], D[i, :].sum() / (n-1)) for i in range(n)]
    tool_avgs.sort(key=lambda pair: pair[1])  # smallest sum first

    with open(output_file, "w") as f:
        f.write(f"MDS stress: {stress}\n")
        f.write(f"Average dPos: {avg_dpos}\n\n")
        f.write("MSA tool average dPos (smallest to largest):\n")
        for tool, avg in tool_avgs:
            f.write(f"{tool}\t{avg}\n")

#Args
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="The input csv file containing the pairwise distances between MSAs", required=False)
parser.add_argument("-o", "--output", help="The output directory for the graphs", required=False)
parser.add_argument("-n", "--np_intermediate", action="store_true", help="Creates a numpy .npz file with the distance matrix and points list, instead of running all graphs", required=False)
args = parser.parse_args()

# Read the CSV
if args.input:
    df = pd.read_csv(args.input)
else:
    print("No input file provided. Using default 'results/rusty-metal/rusty-metal.csv'.")
    df = pd.read_csv("results/rusty-metal/rusty-metal.csv")
    
if args.output:
    output_dir = args.output
else:
    print("No output directory provided. Using default 'results/graphs/'.")
    output_dir = "MSA_graphs/"

# Strip everything before the final '/' from the filenames
df["msa_a"] = df["msa_a"].str.rsplit("/", n=1).str[-1].str.removesuffix(f".fasta")
df["msa_b"] = df["msa_b"].str.rsplit("/", n=1).str[-1].str.removesuffix(f".fasta")

# Get the set of MSAs
points = sorted(set(df["msa_a"]) | set(df["msa_b"]))

# Create an empty distance matrix
D = pd.DataFrame(
    0.0,
    index=points,
    columns=points
)

# Fill in the distances
for _, row in df.iterrows():
    a = row["msa_a"]
    b = row["msa_b"]
    distance = row["distance"]

    D.loc[a, b] = distance
    D.loc[b, a] = distance

# Convert pandas DataFrame to NumPy array for sklearn MDS, and scipy hierarchical clustering
D = D.to_numpy()

#If using the npz intermediate, create that
if args.np_intermediate:
    # Store matrix and labels together
    np.savez(
        "MSA_distances.npz",
        D=D,
        points=np.array(points)
    )
    print(f"Distance matrix saved to MSA_distances.npz")

#If doing everything in one go, do that
else:
    stress = mds.mds_and_plot(D, points, output_file=f"{output_dir}/MSA_distances.png", output_file_nolines=f"{output_dir}/MSA_distances_nolines.png")
    hierarchical_clustering.hierarchical_and_plot(D, points, output_file=f"{output_dir}/MSA_hierarchical.png")
    write_summary(D, points, stress, output_file=f"{output_dir}/MSA_summary.txt")
    