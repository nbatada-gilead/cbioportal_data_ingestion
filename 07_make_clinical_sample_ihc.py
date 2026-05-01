#!/usr/bin/env python3
import csv
import sys
from pathlib import Path

INFILE = Path(sys.argv[1])
OUTFILE = Path(sys.argv[2])

# All columns we will output (order matters)
OUT_COLS = [
    "PATIENT_ID",
    "SAMPLE_ID",
    "tissue_type",
    "PVR_H_score",
    "PVR_pctp",
    "TIL",
    "smoking_status",
    "alcohol_status",
    "TROP2_H_score",
    "PDL1_TC",
    "TIGIT_IC_pct",
    "TIGIT_pct",
    "histology",
    "PDL1_TPS",
    "PDL1",
]

def patient_id_from_sample(sample_id):
    # FT-SA1325982B -> 1325982
    return "".join([c for c in sample_id if c.isdigit()])

with open(INFILE, newline="") as fin, open(OUTFILE, "w", newline="") as fout:
    reader = csv.DictReader(fin, delimiter="\t")
    writer = csv.writer(fout, delimiter="\t")

    # ---- write clinical header ----
    writer.writerow([
        "#Patient Identifier",
        "Sample Identifier",
        *OUT_COLS[2:]
    ])
    writer.writerow([
        "#Unique patient ID",
        "Unique sample ID",
        "Tissue type",
        "PVR H score",
        "PVR percent",
        "Tumor infiltrating lymphocytes",
        "Smoking status",
        "Alcohol status",
        "TROP2 H score",
        "PD-L1 TC",
        "TIGIT IC percent",
        "TIGIT percent",
        "Histology",
        "PD-L1 TPS",
        "PD-L1"
    ])
    writer.writerow([
        "#STRING",
        "STRING",
        "STRING",
        "NUMBER",
        "NUMBER",
        "NUMBER",
        "STRING",
        "STRING",
        "NUMBER",
        "NUMBER",
        "NUMBER",
        "NUMBER",
        "STRING",
        "NUMBER",
        "NUMBER"
    ])
    writer.writerow([
        "#1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"
    ])
    writer.writerow(OUT_COLS)

    # ---- data rows ----
    for row in reader:
        raw_sid = row["sample_id"].strip()
        sample_id = f"FT-SA{raw_sid}"
        patient_id = patient_id_from_sample(raw_sid)

        out = [
            patient_id,
            sample_id,
            row.get("tissue_type",""),
            row.get("PVR_H_score",""),
            row.get("PVR_pctp",""),
            row.get("TIL",""),
            row.get("smoking_status",""),
            row.get("alcohol_status",""),
            row.get("TROP2_H_score",""),
            row.get("PDL1_TC",""),
            row.get("TIGIT_IC_pct",""),
            row.get("TIGIT_pct",""),
            row.get("histology",""),
            row.get("PDL1_TPS",""),
            row.get("PDL1",""),
        ]

        writer.writerow(out)
        
