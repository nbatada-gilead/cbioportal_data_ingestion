#!/usr/bin/env python3

import pandas as pd
import re
import sys
from pathlib import Path

def is_valid_hugo(symbol: str) -> bool:
    """
    Conservative HUGO symbol check:
    - exclude empty
    - exclude obvious non-genes (e.g., chr*, LOC*)
    """
    if pd.isna(symbol):
        return False
    if symbol == "":
        return False
    if symbol.startswith(("chr", "LOC")):
        return False
    return True

def main():
    if len(sys.argv) != 3:
        sys.exit(
            "Usage: 03_expression_use_hugo.py "
            "<expression_tpm_renamed.tsv> <out_prefix>"
        )

    in_path = Path(sys.argv[1])
    out_prefix = Path(sys.argv[2])

    df = pd.read_csv(in_path, sep="\t")

    if "gene_name" not in df.columns:
        sys.exit("Missing required column: gene_name")

    sample_cols = [c for c in df.columns if c not in ("gene_id", "gene_name")]

    qc = pd.DataFrame({
        "gene_name": df["gene_name"],
        "kept": df["gene_name"].map(is_valid_hugo)
    })

    df = df[qc["kept"]].copy()

    # Final matrix: gene symbol + samples
    out = df[["gene_name"] + sample_cols]
    out = out.rename(columns={"gene_name": "Hugo_Symbol"})

    out.to_csv(f"{out_prefix}.tsv", sep="\t", index=False)
    qc.to_csv(f"{out_prefix}_qc.tsv", sep="\t", index=False)

    print(f"Wrote {out_prefix}.tsv")
    print(f"Genes kept: {out.shape[0]}")

if __name__ == "__main__":
    main()
