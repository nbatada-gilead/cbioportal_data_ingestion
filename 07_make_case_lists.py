#!/usr/bin/env python3

import pandas as pd
import sys
from pathlib import Path

def read_cbio_table(path):
    # skip 2-line cbio header if present
    with open(path) as f:
        first = f.readline()
        second = f.readline()
    if first.startswith("#") and second.startswith("#"):
        return pd.read_csv(path, sep="\t", header=2)
    return pd.read_csv(path, sep="\t")

def write_case_list(path, case_ids, stable_id, name):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(f"cancer_study_identifier: {stable_id}\n")
        f.write(f"stable_id: {stable_id}_{name}\n")
        f.write(f"case_list_name: {name}\n")
        f.write(f"case_list_description: {name}\n")
        f.write("case_list_ids: ")
        f.write("\t".join(sorted(case_ids)))
        f.write("\n")

def main():
    if len(sys.argv) != 6:
        sys.exit(
            "Usage: 07_make_case_lists.py "
            "<clinical_sample.txt> <data_mutations.txt> <expression_zscores.tsv> "
            "<output_dir> <study_id>"
        )

    clinical_path, mut_path, expr_path, out_dir, study_id = map(Path, sys.argv[1:6])

    clinical = read_cbio_table(clinical_path)
    all_samples = set(clinical["SAMPLE_ID"].astype(str))

    muts = pd.read_csv(mut_path, sep="\t")
    sequenced = set(muts["Tumor_Sample_Barcode"].astype(str))

    expr = pd.read_csv(expr_path, sep="\t")
    expr_samples = set(expr.columns) - {"Hugo_Symbol"}

    out_dir = Path(out_dir)
    write_case_list(out_dir / "all.txt", all_samples, study_id, "all")
    write_case_list(out_dir / "sequenced.txt", all_samples & sequenced, study_id, "sequenced")
    write_case_list(out_dir / "expression.txt", all_samples & expr_samples, study_id, "expression")

    print("Case lists written:")
    print(f"  all: {len(all_samples)}")
    print(f"  sequenced: {len(all_samples & sequenced)}")
    print(f"  expression: {len(all_samples & expr_samples)}")

if __name__ == "__main__":
    main()
    
