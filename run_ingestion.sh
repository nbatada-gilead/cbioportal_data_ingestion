#!/usr/bin/env bash
# Nizar Batada
# 1 May 2026

set -euo pipefail

# run from the project folder
DIR_PROJECT="$(cd "$(dirname "$0")" && pwd)"
source "${DIR_PROJECT}/config/project_setup_parameters.txt"

DIR_REPO="${HOME}/git/cbioportal_data_ingestion"
DIR_SCRIPTS="${DIR_REPO}/scripts"
DIR_RAW="${DIR_PROJECT}/unformatted_files"
DIR_OUT="${DIR_PROJECT}/output"
DIR_LOG="${DIR_PROJECT}/logs"

mkdir -p "${DIR_OUT}" "${DIR_LOG}"

log() { echo "[$(date)] $*" | tee -a "${DIR_LOG}/pipeline.log"; }

# ---------------------------
# Step 1: Harmonize samples (RNA)
# ---------------------------
log "Step 1: Harmonize RNA samples"
python "${DIR_SCRIPTS}/01_harmonize_samples.py" \
  "${DIR_RAW}/${FULGENT_QC_CSV}" \
  "${DIR_OUT}/harmonized_samples.tsv"

# ---------------------------
# Step 1b: Add WES samples (optional)
# ---------------------------
if [[ "${HAS_WES}" == "true" ]]; then
  log "Step 1b: Add WES samples from samplesheet"
  python "${DIR_SCRIPTS}/01b_add_wes_samples.py" \
    "${DIR_OUT}/harmonized_samples.tsv" \
    "${DIR_RAW}/${WES_SAMPLESHEET}" \
    "${DIR_RAW}/${PATIENT_METADATA}" \
    "${DIR_OUT}/harmonized_samples_with_wes.tsv"
else
  cp "${DIR_OUT}/harmonized_samples.tsv" "${DIR_OUT}/harmonized_samples_with_wes.tsv"
fi

# ---------------------------
# Step 2-4: RNAseq (optional)
# ---------------------------
if [[ "${HAS_RNASEQ}" == "true" ]]; then
  log "Step 2: Reconcile expression sample IDs"
  python "${DIR_SCRIPTS}/02_reconcile_expression_samples.py" \
    "${DIR_RAW}/${RNASEQ_TPM_TSV}" \
    "${DIR_OUT}/harmonized_samples.tsv" \
    "${DIR_OUT}/expression_tpm_renamed"

  log "Step 3: Use HUGO symbols"
  python "${DIR_SCRIPTS}/03_expression_use_hugo.py" \
    "${DIR_OUT}/expression_tpm_renamed.tsv" \
    "${DIR_OUT}/expression_tpm_gene_symbol"

  log "Step 4: Compute z-scores"
  python "${DIR_SCRIPTS}/04_expression_zscore.py" \
    "${DIR_OUT}/expression_tpm_gene_symbol.tsv" \
    "${DIR_OUT}/expression_zscores"
fi

# ---------------------------
# Step 5: Clinical tables
# ---------------------------
log "Step 5: Build clinical patient + sample"
python "${DIR_SCRIPTS}/05_build_clinical.py" \
  "${DIR_OUT}/harmonized_samples_with_wes.tsv" \
  "${DIR_RAW}/${PATIENT_METADATA}" \
  "${DIR_OUT}/data_clinical_patient.txt" \
  "${DIR_OUT}/data_clinical_sample.txt"

# ---------------------------
# Step 5b: IHC (optional) -> merge into sample clinical file
# ---------------------------
if [[ "${HAS_IHC}" == "true" ]]; then
  log "Step 5b: Build IHC sample clinical"
  python "${DIR_SCRIPTS}/07_make_clinical_sample_ihc.py" \
    "${DIR_RAW}/${IHC_FILE}" \
    "${DIR_OUT}/data_clinical_sample_ihc.txt"

  log "Step 5c: Merge IHC into sample clinical"
  python "${DIR_SCRIPTS}/07_merge_sample_clinical_with_ihc.py" \
    "${DIR_OUT}/data_clinical_sample.txt" \
    "${DIR_OUT}/data_clinical_sample_ihc.txt" \
    "${DIR_OUT}/data_clinical_sample.txt"
fi

# ---------------------------
# Step 6: Mutations (optional)
# ---------------------------
MUT_FILE=""
if [[ "${HAS_WES}" == "true" ]]; then
  log "Step 6: Build slim mutations from per-sample MAFs"
  python "${DIR_SCRIPTS}/06_from_mafs_build_slim_mutations.py" \
    "${DIR_RAW}/${WES_MAF_DIR}" \
    "${DIR_OUT}/harmonized_samples_with_wes.tsv" \
    "${DIR_OUT}/data_mutations.slim.from_mafs.txt"
  MUT_FILE="data_mutations.slim.from_mafs.txt"
fi

# ---------------------------
# Step 7: Case lists
# ---------------------------
log "Step 7: Case lists"
python "${DIR_SCRIPTS}/07_make_case_lists.py" \
  "${DIR_OUT}/data_clinical_sample.txt" \
  "${DIR_OUT}/${MUT_FILE}" \
  "${DIR_OUT}/expression_zscores.tsv" \
  "${DIR_OUT}/case_lists" \
  "${PROJECT_NAME}"

# ---------------------------
# Step 8: Meta files
# ---------------------------
log "Step 8: Write meta files"

cat > "${DIR_OUT}/meta_study.txt" <<EOF
type_of_cancer: ${TYPE_OF_CANCER}
cancer_study_identifier: ${PROJECT_NAME}
name: ${STUDY_NAME}
description: ${STUDY_DESCRIPTION}
reference_genome: ${REFERENCE_GENOME}
add_global_case_list: false
EOF

cat > "${DIR_OUT}/meta_clinical_patient.txt" <<EOF
cancer_study_identifier: ${PROJECT_NAME}
genetic_alteration_type: CLINICAL
datatype: PATIENT_ATTRIBUTES
data_filename: data_clinical_patient.txt
EOF

cat > "${DIR_OUT}/meta_clinical_sample.txt" <<EOF
cancer_study_identifier: ${PROJECT_NAME}
genetic_alteration_type: CLINICAL
datatype: SAMPLE_ATTRIBUTES
data_filename: data_clinical_sample.txt
EOF

if [[ "${HAS_RNASEQ}" == "true" ]]; then
cat > "${DIR_OUT}/meta_expression.txt" <<EOF
cancer_study_identifier: ${PROJECT_NAME}
genetic_alteration_type: MRNA_EXPRESSION
datatype: Z-SCORE
stable_id: mrna_seq_tpm_all_sample_Zscores
show_profile_in_analysis_tab: true
profile_name: mRNA expression z-scores
profile_description: Gene-level mRNA expression z-scores from RNA-seq TPM (all-sample reference)
data_filename: expression_zscores.tsv
EOF
fi

if [[ "${HAS_WES}" == "true" ]]; then
cat > "${DIR_OUT}/meta_mutations.txt" <<EOF
cancer_study_identifier: ${PROJECT_NAME}
genetic_alteration_type: MUTATION_EXTENDED
datatype: MAF
stable_id: mutations
show_profile_in_analysis_tab: true
profile_name: Somatic mutations (WES)
profile_description: Somatic mutations from whole-exome sequencing
data_filename: ${MUT_FILE}
EOF
fi

# ---------------------------
# Validation (optional)
# ---------------------------
if [[ "${RUN_VALIDATION}" == "true" ]]; then
  log "Validate"
  ( cd "${VALIDATOR_DIR}" && ./validateData.py -s "${DIR_OUT}" ${VALIDATOR_FLAGS} )
fi

log "DONE"
