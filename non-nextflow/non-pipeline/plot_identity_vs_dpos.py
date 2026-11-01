from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", nargs="+", default=["saved-results/PID vs avg dPos graphs/NCBI and BLAST.csv", "saved-results/PID vs avg dPos graphs/BAliBASE.csv", "saved-results/PID vs avg dPos graphs/Alisim.csv"])
    parser.add_argument("-o", "--output", default="identity_vs_dpos_regression_3.png")
    args = parser.parse_args()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    markers = ['o', 's', '^', 'D', 'v', 'P', 'X', '*']

    for i, input_file in enumerate(args.input):
        df = pd.read_csv(input_file)
        label = Path(input_file).stem
        color = colors[i % len(colors)]
        marker = markers[i % len(markers)]

        x = df["percent_identity"]
        y = df["average_dpos"]

        result = stats.linregress(x, y)
        spearman = stats.spearmanr(x, y)

        ax.scatter(x, y, alpha=0.7, color=color, marker=marker, label=label)

        x_line = [x.min(), x.max()]
        y_line = [result.intercept + result.slope * xi for xi in x_line]
        sign = '+' if result.intercept >= 0 else '-'
        equation = f"y = {result.slope:.4f}x {sign} {abs(result.intercept):.4f}"
        ax.plot(x_line, y_line, color=color, linestyle='--',
                label=f"{equation}\nr = {result.rvalue:.3f}")

        print(f"[{label}] Pearson r  = {result.rvalue:.4f}  (p = {result.pvalue:.4g})")
        print(f"[{label}] Spearman r = {spearman.correlation:.4f}  (p = {spearman.pvalue:.4g})")

    ax.set_xlabel("Percent identity")
    ax.set_ylabel("Average ensemble dpos")
    ax.legend()

    plt.tight_layout()
    plt.savefig(args.output, dpi=200)
    
    print(f"Saved plot to {args.output}")


if __name__ == "__main__":
    main()
