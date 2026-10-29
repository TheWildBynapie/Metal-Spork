import argparse
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="identity_vs_dpos.csv")
    parser.add_argument("-o", "--output", default="identity_vs_dpos_regression.png")
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    x = df["percent_identity"]
    y = df["average_dpos"]

    result = stats.linregress(x, y)
    spearman = stats.spearmanr(x, y)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y, alpha=0.7)

    x_line = [x.min(), x.max()]
    y_line = [result.intercept + result.slope * xi for xi in x_line]
    ax.plot(x_line, y_line, color='red', linestyle='--', label=f"r = {result.rvalue:.3f}")

    ax.set_xlabel("Percent identity")
    ax.set_ylabel("Average ensemble dpos")
    ax.legend()

    plt.tight_layout()
    plt.savefig(args.output, dpi=200)

    print(f"Pearson r  = {result.rvalue:.4f}  (p = {result.pvalue:.4g})")
    print(f"Spearman r = {spearman.correlation:.4f}  (p = {spearman.pvalue:.4g})")
    print(f"Saved plot to {args.output}")


if __name__ == "__main__":
    main()
