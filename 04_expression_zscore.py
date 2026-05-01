#!/usr/bin/env python3

import pandas as pd
import numpy as np
import sys
from pathlib import Path

def main():
    if len(sys.argv) != 3:
        sys.exit(
            "Usage: 04_expression_zscore.py "
            "<expression_tpm_gene_symbol.tsv> <out_prefix>"
        )

    in_path = Path(sys.argv[1])
    out_prefix = Path(sys.argv[2])

    df = pd.read_csv(in_path, sep="\t")

    if "Hugo_Symbol" not in df.columns:
        sys.exit("Missing required column: Hugo_Symbol")

    genes = df["Hugo_Symbol"]
    X = df.drop(columns=["Hugo_Symbol"]).astype(float)

    means = X.mean(axis=1)
    stds = X.std(axis=1, ddof=0)

    keep = stds > 0

    Z = X.sub(means, axis=0).div(stds, axis=0)

    out = pd.concat([genes[keep].reset_index(drop=True),
                     Z.loc[keep].reset_index(drop=True)], axis=1)

    qc = pd.DataFrame({
        "Hugo_Symbol": genes,
        "mean": means,
        "std": stds,
        "kept": keep
    })

    out.to_csv(f"{out_prefix}.tsv", sep="\t", index=False)
    qc.to_csv(f"{out_prefix}_qc.tsv", sep="\t", index=False)

    print(f"Wrote {out_prefix}.tsv")
    print(f"Genes kept: {keep.sum()} / {len(keep)}")

if __name__ == "__main__":
    main()
    
