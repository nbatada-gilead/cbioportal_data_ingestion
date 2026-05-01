#!/usr/bin/env python3

import pandas as pd
import sys
from pathlib import Path

def main():
    if len(sys.argv) != 5:
        sys.exit(
            "Usage: 05_build_clinical.py "
            "<harmonized_samples.tsv> <patient_metadata.tsv> "
            "<out_patient.txt> <out_sample.txt>"
        )

    harmonized_path = Path(sys.argv[1])
    patient_meta_path = Path(sys.argv[2])
    out_patient = Path(sys.argv[3])
    out_sample = Path(sys.argv[4])

    samples = pd.read_csv(harmonized_path, sep="\t")
    patients = pd.read_csv(patient_meta_path, sep=None, engine="python")


    # ----------------------
    # Patient clinical table
    # ----------------------
    patient_clin = patients[["patient_id"]].drop_duplicates()
    patient_clin = patient_clin.rename(columns={
        "patient_id": "PATIENT_ID"
    })

    # cbio header lines
    patient_header = [
        "#Patient Identifier",
        "#Unique patient ID"
    ]

    with open(out_patient, "w") as f:
        for h in patient_header:
            f.write(h + "\n")
        patient_clin.to_csv(f, sep="\t", index=False)

    # ----------------------
    # Sample clinical table
    # ----------------------
    sample_clin = pd.DataFrame({
        "PATIENT_ID": samples["PATIENT_ID"],
        "SAMPLE_ID": samples["SAMPLE_ID"],
        "CANCER_TYPE": "Lung",
        "ONCOTREE_CODE": "LUAD",
        "SAMPLE_TYPE": samples["ASSAY_TYPE"]
    })

    sample_header = [
        "#Patient Identifier\tSample Identifier\tCancer Type\tOncotree Code\tSample Type",
        "#Unique patient ID\tUnique sample ID\tCancer type\tOncoTree code\tSample type"
    ]

    with open(out_sample, "w") as f:
        for h in sample_header:
            f.write(h + "\n")
        sample_clin.to_csv(f, sep="\t", index=False)

    print("Wrote clinical files:")
    print(f"  {out_patient}")
    print(f"  {out_sample}")

if __name__ == "__main__":
    main()

    
