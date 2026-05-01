#!/usr/bin/env python3

import pandas as pd
import re
import sys
from pathlib import Path

def normalize_fulgent_id(x: str) -> str:
    """
    Normalize Fulgent sample IDs:
    FT.SA334010R  → FT-SA334010R
    """
    if pd.isna(x):
        return x
    return re.sub(r'^FT\.SA', 'FT-SA', x)

def main():
    if len(sys.argv) != 3:
        sys.exit(
            "Usage: 01_harmonize_samples.py <fulgent_qc_samples.csv> <output_tsv>"
        )

    infile = Path(sys.argv[1])
    outfile = Path(sys.argv[2])

    df = pd.read_csv(infile)

    # Required columns check
    required = [
        "accessionid",
        "patient_id",
        "sample_id",
        "externalspecimenid",
        "sampletype",
        "paired_normal_accessionid"
    ]
    missing = set(required) - set(df.columns)
    if missing:
        sys.exit(f"Missing required columns: {missing}")

    out = pd.DataFrame({
        "PATIENT_ID": df["patient_id"],
        "SAMPLE_ID": df["accessionid"].map(normalize_fulgent_id),
        "FULGENT_ACCESSION_ID": df["accessionid"],
        "INTERNAL_SAMPLE_ID": df["sample_id"],
        "EXTERNAL_SPECIMEN_ID": df["externalspecimenid"],
        "ASSAY_TYPE": df["sampletype"],
        "NORMAL_SAMPLE_ID": df["paired_normal_accessionid"].map(normalize_fulgent_id),
        "BATCH_ID": df.get("sample_plateid", None)
    })

    out = out.drop_duplicates()

    out.to_csv(outfile, sep="\t", index=False)

    print(f"Wrote {outfile}")
    print(f"Samples: {out.shape[0]}")

if __name__ == "__main__":
    main()

    
