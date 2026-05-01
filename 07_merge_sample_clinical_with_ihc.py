#!/usr/bin/env python3
import sys
import csv

BASE = sys.argv[1]
IHC  = sys.argv[2]
OUT  = sys.argv[3]

def read_clinical_sample(path):
    """
    Find the real header line containing SAMPLE_ID,
    then read the table into a dict keyed by SAMPLE_ID.
    """
    rows = {}

    with open(path) as f:
        # advance until we hit the actual column header
        for line in f:
            if line.startswith("PATIENT_ID") and "SAMPLE_ID" in line:
                header = line.rstrip("\n").split("\t")
                break
        else:
            raise RuntimeError(f"Could not find header with SAMPLE_ID in {path}")

        reader = csv.DictReader(f, delimiter="\t", fieldnames=header)

        for row in reader:
            rows[row["SAMPLE_ID"]] = row

    return rows

base_rows = read_clinical_sample(BASE)
ihc_rows  = read_clinical_sample(IHC)

IHC_COLS = [
    "TISSUE_TYPE",
    "PVR_H_SCORE",
    "PVR_PCTP",
    "TIL",
    "SMOKING_STATUS",
    "ALCOHOL_STATUS",
    "TROP2_H_SCORE",
    "PDL1_TC",
    "TIGIT_IC_PCT",
    "TIGIT_PCT",
    "HISTOLOGY",
    "PDL1_TPS",
    "PDL1",
]

with open(OUT, "w", newline="") as fout:
    writer = csv.writer(fout, delimiter="\t")

    # ---- HEADER ----
    writer.writerow(["#Patient Identifier","Sample Identifier", *IHC_COLS])
    writer.writerow([
        "#Unique patient ID","Unique sample ID",
        "Tissue type","PVR H score","PVR percent","TIL",
        "Smoking status","Alcohol status",
        "TROP2 H score","PD-L1 TC",
        "TIGIT IC percent","TIGIT percent","Histology",
        "PD-L1 TPS","PD-L1"
    ])
    writer.writerow([
        "#STRING","STRING",
        "STRING","NUMBER","NUMBER","NUMBER",
        "STRING","STRING",
        "NUMBER","NUMBER",
        "NUMBER","NUMBER","STRING",
        "NUMBER","NUMBER"
    ])
    writer.writerow(["#1","1"] + ["1"] * len(IHC_COLS))
    writer.writerow(["PATIENT_ID","SAMPLE_ID", *IHC_COLS])

    # ---- DATA ----
    for sid, base in base_rows.items():
        ihc = ihc_rows.get(sid, {})

        out = [
            base["PATIENT_ID"],
            sid,
            ihc.get("tissue_type",""),
            ihc.get("pvr_h_score",""),
            ihc.get("pvr_pctp",""),
            ihc.get("til",""),
            ihc.get("smoking_status",""),
            ihc.get("alcohol_status",""),
            ihc.get("trop2_h_score",""),
            ihc.get("pdl1_tc",""),
            ihc.get("tigit_ic_pct",""),
            ihc.get("tigit_pct",""),
            ihc.get("histology",""),
            ihc.get("pdl1_tps",""),
            ihc.get("pdl1",""),
        ]

        writer.writerow(out)
