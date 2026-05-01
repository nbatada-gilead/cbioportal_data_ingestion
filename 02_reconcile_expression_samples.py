#!/usr/bin/env python3

import pandas as pd
import re
import sys
from pathlib import Path

def normalize_expr_sample_id(x: str) -> str:
    """
    FT.SA334010R -> FT-SA334010R
    """
    return re.sub(r'^FT\.SA', 'FT-SA', x)

def main():
    if len(sys.argv) != 4:
        sys.exit(
            "Usage: 02_reconcile_expression_samples.py "
            "<expression_tpm.tsv> <harmonized_samples.tsv> <out_prefix>"
        )

    expr_path = Path(sys.argv[1])
    map_path = Path(sys.argv[2])
    out_prefix = Path(sys.argv[3])

    expr = pd.read_csv(expr_path, sep="\t")
    sample_map = pd.read_csv(map_path, sep="\t")

    canonical_samples = set(sample_map["SAMPLE_ID"])

    # Identify expression sample columns
    fixed_cols = ["gene_id", "gene_name"]
    expr_sample_cols = [c for c in expr.columns if c not in fixed_cols]

    rename_map = {
        c: normalize_expr_sample_id(c)
        for c in expr_sample_cols
    }

    expr_renamed = expr.rename(columns=rename_map)

    keep_samples = [
        c for c in rename_map.values()
        if c in canonical_samples
    ]

    expr_final = expr_renamed[fixed_cols + keep_samples]

    # Write outputs
    expr_final.to_csv(
        f"{out_prefix}.tsv",
        sep="\t",
        index=False
    )

    pd.DataFrame({
        "original_sample_id": expr_sample_cols,
        "normalized_sample_id": [rename_map[c] for c in expr_sample_cols],
        "kept": [rename_map[c] in canonical_samples for c in expr_sample_cols]
    }).to_csv(
        f"{out_prefix}_sample_map.tsv",
        sep="\t",
        index=False
    )

    print(f"Kept {len(keep_samples)} expression samples")
    print(f"Wrote {out_prefix}.tsv")

if __name__ == "__main__":
    main()
