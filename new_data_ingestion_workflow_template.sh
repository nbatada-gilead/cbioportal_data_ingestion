#!/usr/bin/env bash
set -euo pipefail

############################################
# STUDY‑LEVEL METADATA
############################################

STUDY_ID="lung_translational"
CANCER_TYPE="lung"
ONCOTREE_DEFAULT="LUAD"

############################################
# RAW (UNFORMATTED) INPUT FILES
############################################

# 1) Fulgent / sequencing QC table (RNAseq + WES)
UNFORMATTED_SAMPLE_INFO_PATH=""

# 2) Patient metadata table (free‑form columns)
UNFORMATTED_PATIENT_INFO_PATH=""

# 3) IHC table (optional)
UNFORMATTED_IHC_INFO_PATH=""

# 4) Gene expression (TPM)
UNFORMATTED_EXPRESSION_TPM_PATH=""

# 5) Mutation inputs (directory containing many batch MAFs)
UNFORMATTED_MAF_ROOT_PATH=""

############################################
# ADaM (OPTIONAL – CAN BE EMPTY FOR NOW)
############################################

ADAM_PATIENT_LEVEL_PATH=""
ADAM_SURVIVAL_LEVEL_PATH=""

############################################
# COLUMN MAPPINGS (RAW → CANONICAL)
############################################
# These MUST be edited per dataset

# ---- Sample mapping (Fulgent / QC table) ----
COL_SAMPLE_SOURCE_SAMPLE_ID="accessionid"
COL_SAMPLE_PATIENT_ID="patient_id"
COL_SAMPLE_SAMPLE_ID="externalspecimenid"
COL_SAMPLE_ASSAY_TYPE="sampletype"
COL_SAMPLE_BATCH_ID="sample_plateid"

# ---- Patient metadata ----
COL_PATIENT_PATIENT_ID="patient_id"

# ---- Expression matrix ----
EXPR_SAMPLE_ID_COLUMN="sample_id"
EXPR_GENE_ID_TYPE="ENSG"     # ENSG | SYMBOL
EXPR_VALUE_TYPE="TPM"

############################################
# REFERENCE FILES
############################################

ENSG_TO_HGNC_MAP="reference/ensg_to_hgnc.tsv"
ONCOTREE_MAP="reference/oncotree_map.tsv"

############################################
# OUTPUT
############################################

OUT_STUDY_DIR="output/${STUDY_ID}"

############################################
# PIPELINE STEPS (NO IMPLEMENTATION YET)
############################################

echo "Preparing study: ${STUDY_ID}"
echo "Output directory: ${OUT_STUDY_DIR}"

# Placeholder – steps will be added incrementally
# python steps/01_ids.py
# python steps/02_clinical.py
# python steps/03_expression.py
# python steps/04_mutations.py
# python steps/05_caselists.py
# python steps/06_meta.py
