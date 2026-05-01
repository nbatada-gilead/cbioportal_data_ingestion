#!/usr/bin/env python3

import pandas as pd
import re
import sys
from pathlib import Path

def norm_ft(x: str) -> str:
    if pd.isna(x):
        return x
    x = str(x)
    x = re.sub(r"^FT\.SA", "FT-SA", x)
    return x

def extract_wes_sample_id(sample_field: str) -> str:
    x = norm_ft(sample_field)
    x = re.sub(r"_\d+$", "", x)
    return x

def extract_internal_sample_id_from_fastq(fastq_path: str) -> str:
    if pd.isna(fastq_path):
        return None
    s = str(fastq_path)
    m = re.search(r"/([^/]+?)-250", s)
    if m:
        return m.group(1)
    m = re.search(r"/([^/]+?)_", s)
    if m:
        return m.group(1)
    return None

def read_table_auto(path: Path):
    return pd.read_csv(path, sep=None, engine="python")

def main():
    if len(sys.argv) != 5:
        sys.exit(
            "Usage: 01b_add_wes_samples.py "
            "<harmonized_samples.tsv> <samplesheet_wes.csv> <patient_metadata.tsv> <out_tsv>"
        )

    harmonized_path = Path(sys.argv[1])
    wes_sheet_path = Path(sys.argv[2])
    patient_meta_path = Path(sys.argv[3])
    out_path = Path(sys.argv[4])

    harmonized = pd.read_csv(harmonized_path, sep="\t")
    wes = read_table_auto(wes_sheet_path)
    pm = read_table_auto(patient_meta_path)

    if "sample" not in wes.columns or "fastq_1" not in wes.columns:
        sys.exit("samplesheet_wes.csv must have columns: sample, fastq_1")

    if "sample_id" not in pm.columns or "patient_id" not in pm.columns:
        sys.exit("patient_metadata must have columns: sample_id, patient_id")

    wes = wes.copy()
    wes["WES_SAMPLE_ID"] = wes["sample"].map(extract_wes_sample_id)
    wes["INTERNAL_SAMPLE_ID"] = wes["fastq_1"].map(extract_internal_sample_id_from_fastq)

    wes_tumor = wes
    if "status" in wes_tumor.columns:
        wes_tumor = wes_tumor[wes_tumor["status"].astype(str).isin(["1", "1.0"])].copy()

    wes_tumor = wes_tumor.merge(
        pm[["sample_id", "patient_id"]].rename(columns={"sample_id": "INTERNAL_SAMPLE_ID", "patient_id": "PATIENT_ID_FROM_PM"}),
        on="INTERNAL_SAMPLE_ID",
        how="left"
    )

    if "patient" in wes_tumor.columns:
        wes_tumor["PATIENT_ID"] = wes_tumor["PATIENT_ID_FROM_PM"].fillna(wes_tumor["patient"])
    else:
        wes_tumor["PATIENT_ID"] = wes_tumor["PATIENT_ID_FROM_PM"]

    out_rows = pd.DataFrame({
        "PATIENT_ID": wes_tumor["PATIENT_ID"],
        "SAMPLE_ID": wes_tumor["WES_SAMPLE_ID"].map(norm_ft),
        "FULGENT_ACCESSION_ID": wes_tumor["WES_SAMPLE_ID"].map(norm_ft),
        "INTERNAL_SAMPLE_ID": wes_tumor["INTERNAL_SAMPLE_ID"],
        "EXTERNAL_SPECIMEN_ID": "",
        "ASSAY_TYPE": "WES",
        "NORMAL_SAMPLE_ID": "",
        "BATCH_ID": wes_tumor["lane"] if "lane" in wes_tumor.columns else ""
    }).dropna(subset=["SAMPLE_ID", "INTERNAL_SAMPLE_ID"]).drop_duplicates()

    combined = pd.concat([harmonized, out_rows], ignore_index=True).drop_duplicates(
        subset=["SAMPLE_ID", "ASSAY_TYPE"], keep="first"
    )

    combined.to_csv(out_path, sep="\t", index=False)

    print(f"Wrote {out_path}")
    print(f"Total rows: {combined.shape[0]}")
    print(f"WES rows: {(combined['ASSAY_TYPE'] == 'WES').sum()}")

if __name__ == "__main__":
    main()
