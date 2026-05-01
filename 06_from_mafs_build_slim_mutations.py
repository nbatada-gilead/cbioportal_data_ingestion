#!/usr/bin/env python3
import gzip
import sys
import re
from pathlib import Path

# Required by validator: at least one of HGVSp_Short or Amino_Acid_Change.
# We'll include HGVSp_Short.
OUT_COLS = [
    "Hugo_Symbol",
    "Chromosome",
    "Start_Position",
    "End_Position",
    "Variant_Classification",
    "Variant_Type",
    "Reference_Allele",
    "Tumor_Seq_Allele2",
    "Tumor_Sample_Barcode",
    "HGVSp_Short",     # <-- fixes the validator ERROR
    "SWISSPROT",       # optional but removes validator warning if present
]

# These types are filtered by cbioportal anyway; filtering here reduces file size.
FILTERED_CLASSIFICATIONS = set(["Silent", "Intron", "3'UTR", "3'Flank", "5'UTR", "5'Flank", "IGR", "RNA"])

def ids_from_filename(maf_name: str):
    base = maf_name
    if base.endswith(".gz"):
        base = base[:-3]
    if base.endswith(".maf"):
        base = base[:-4]
    m = re.search(r"(FT[-\.]SA\d{6}[DR]?)(?:_\d+)?_vs_(FT[-\.]SA\d{6}[DR]?)(?:_\d+)?", base)
    if not m:
        return (None, None)
    tumor = re.sub(r"^FT\.SA", "FT-SA", m.group(1)).split("_")[0]
    normal = re.sub(r"^FT\.SA", "FT-SA", m.group(2)).split("_")[0]
    return (tumor, normal)

def to_ascii(s: str) -> str:
    if s is None:
        return ""
    return str(s).encode("ascii", "ignore").decode("ascii")

def load_valid_samples(harmonized_path: Path):
    valid = set()
    with open(harmonized_path, "r", encoding="utf-8", errors="replace") as f:
        hdr = f.readline().rstrip("\n").split("\t")
        idx = {c:i for i,c in enumerate(hdr)}
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == len(hdr):
                valid.add(parts[idx["SAMPLE_ID"]])
    return valid

def find_header(fin):
    for line in fin:
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        cols = line.split("\t")
        if "Hugo_Symbol" in cols and "Tumor_Sample_Barcode" in cols:
            return cols
    return None

def main():
    if len(sys.argv) != 4:
        sys.exit("Usage: 06_from_mafs_build_slim_mutations.py <maf_root_dir> <harmonized_samples_with_wes.tsv> <out_txt>")

    maf_root = Path(sys.argv[1])
    harmonized = Path(sys.argv[2])
    out_path = Path(sys.argv[3])

    valid_samples = load_valid_samples(harmonized)
    if not valid_samples:
        sys.exit("No valid SAMPLE_IDs loaded from harmonized_samples_with_wes.tsv")

    maf_files = sorted(maf_root.rglob("*.maf.gz"))
    if not maf_files:
        sys.exit(f"No .maf.gz found under {maf_root}")

    wrote_header = False
    rows_written = 0
    files_used = 0

    with open(out_path, "w", encoding="utf-8", errors="strict") as fout:
        fout.write("\t".join(OUT_COLS) + "\n")
        wrote_header = True

        for i, maf in enumerate(maf_files, start=1):
            tumor_id, _ = ids_from_filename(maf.name)
            if tumor_id is None:
                continue

            with gzip.open(maf, "rt", encoding="utf-8", errors="replace") as fin:
                cols = find_header(fin)
                if cols is None:
                    continue
                idx = {c:j for j,c in enumerate(cols)}

                # required cols we must have in every file
                required = [
                    "Hugo_Symbol","Chromosome","Start_Position","End_Position",
                    "Variant_Classification","Variant_Type","Reference_Allele",
                    "Tumor_Seq_Allele2","Tumor_Sample_Barcode"
                ]
                if any(c not in idx for c in required):
                    continue

                # optional cols
                has_hgvsp = "HGVSp_Short" in idx
                has_swiss = "SWISSPROT" in idx

                tumor_col = idx["Tumor_Sample_Barcode"]
                vc_col = idx["Variant_Classification"]

                n_file = 0
                for line in fin:
                    parts = line.rstrip("\n").split("\t")
                    if len(parts) != len(cols):
                        continue

                    # override placeholder barcode
                    if parts[tumor_col].upper() == "TUMOR":
                        parts[tumor_col] = tumor_id

                    # normalize barcode suffix
                    parts[tumor_col] = re.sub(r"_\d+$", "", parts[tumor_col]).split("_")[0]
                    parts[tumor_col] = re.sub(r"^FT\.SA", "FT-SA", parts[tumor_col])

                    # keep only samples present in clinical
                    if parts[tumor_col] not in valid_samples:
                        continue

                    # drop types cbioportal will filter anyway (shrinks file)
                    if parts[vc_col] in FILTERED_CLASSIFICATIONS:
                        continue

                    out = [
                        parts[idx["Hugo_Symbol"]],
                        parts[idx["Chromosome"]],
                        parts[idx["Start_Position"]],
                        parts[idx["End_Position"]],
                        parts[idx["Variant_Classification"]],
                        parts[idx["Variant_Type"]],
                        parts[idx["Reference_Allele"]],
                        parts[idx["Tumor_Seq_Allele2"]],
                        parts[idx["Tumor_Sample_Barcode"]],
                        parts[idx["HGVSp_Short"]] if has_hgvsp else "",
                        parts[idx["SWISSPROT"]] if has_swiss else "",
                    ]
                    fout.write("\t".join(to_ascii(x) for x in out) + "\n")
                    n_file += 1

                if n_file > 0:
                    files_used += 1
                    rows_written += n_file

                if i % 25 == 0:
                    print(f"processed={i}/{len(maf_files)} files_used={files_used} rows_written={rows_written}", file=sys.stderr)

    print(f"DONE files={len(maf_files)} files_used={files_used} rows_written={rows_written}", file=sys.stderr)

if __name__ == "__main__":
    main()
    
