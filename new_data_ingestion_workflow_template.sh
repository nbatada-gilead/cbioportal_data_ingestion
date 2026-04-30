#!/usr/bin/env bash
set -euo pipefail

############################################
# GLOBAL PATHS (DO NOT EDIT)
############################################

DIR_ROOT=~/git/cbioportal_data_ingestion
DIR_SCRIPTS=${DIR_ROOT}/scripts
DIR_PROJECTS=${DIR_ROOT}/projects

############################################
# PROJECT CONFIG (EDIT PER PROJECT)
############################################

PROJECT_NAME=""
DIR_PROJECT=${DIR_PROJECTS}/${PROJECT_NAME}

UNFORMATTED_DIR=${DIR_PROJECT}/unformatted_files
OUTPUT_DIR=${DIR_PROJECT}/cbioportal_ready

############################################
# RAW INPUT FILES (EDIT PER PROJECT)
############################################

# Sample / sequencing QC (Fulgent)
UNFORMATTED_SAMPLE_INFO_PATH=""

# Patient metadata (free‑form)
UNFORMATTED_PATIENT_INFO_PATH=""

# IHC table (optional)
UNFORMATTED_IHC_INFO_PATH=""

# Expression (TPM)
UNFORMATTED_EXPRESSION_TPM_PATH=""

# Mutation MAF batches (directory)
UNFORMATTED_MAF_ROOT_PATH=""

############################################
# COLUMN MAPPING (RAW → CANONICAL)
############################################

# ---- Sample info table ----
COL_SAMPLE_SOURCE_SAMPLE_ID="accessionid"
COL_SAMPLE_PATIENT_ID="patient_id"
COL_SAMPLE_SAMPLE_ID="externalspecimenid"
COL_SAMPLE_ASSAY_TYPE="sampletype"
COL_SAMPLE_BATCH_ID="sample_plateid"

# ---- Patient table ----
COL_PATIENT_PATIENT_ID="patient_id"

############################################
# EXPRESSION SETTINGS
############################################

EXPR_GENE_ID_TYPE="ENSG"      # ENSG or SYMBOL
EXPR_VALUE_TYPE="TPM"

############################################
# REFERENCE FILES
############################################

ENSG_TO_HGNC_MAP=${DIR_SCRIPTS}/reference/ensg_to_hgnc.tsv
ONCOTREE_MAP=${DIR_SCRIPTS}/reference/oncotree_map.tsv

############################################
# PIPELINE STEPS (ADDED GRADUALLY)
############################################

echo "Starting ingestion for ${PROJECT_NAME}"
echo "Project directory: ${DIR_PROJECT}"

# Steps will be enabled one‑by‑one
# python ${DIR_SCRIPTS}/steps/01_harmonize_ids.py
# python ${DIR_SCRIPTS}/steps/02_build_clinical.py
# python ${DIR_SCRIPTS}/steps/03_expression_zscores.py
# python ${DIR_SCRIPTS}/steps/04_merge_maf.py
# python ${DIR_SCRIPTS}/steps/05_case_lists.py
# python ${DIR_SCRIPTS}/steps/06_meta_files.py
