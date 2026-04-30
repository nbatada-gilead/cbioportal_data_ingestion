code is in ~/git/cbioportal_data_ingestion
~/projects/cbioportal_ingestion # Actual study runs + data



# Step 1) Define global directories (once, on your machine)
# Root of the whole ingestion repo
DIR_ROOT=~/git/cbioportal_data_ingestion

# Scripts reused for every project
DIR_SCRIPTS=${DIR_ROOT}/scripts

# Where each project lives
DIR_PROJECTS=${DIR_ROOT}/projects


# Step 2) Define new project variables (per study)
PROJECT_NAME=lung_translational
DIR_NEW_PROJECT=${DIR_PROJECTS}/${PROJECT_NAME}

# Step 3) Create project directory + copy workflow template
mkdir -p ${DIR_NEW_PROJECT}

cp ${DIR_SCRIPTS}/new_data_ingestion_workflow_template.sh \
   ${DIR_NEW_PROJECT}/run_ingestion.sh

# Step 4) Create raw‑data staging directory
Step 4) Create raw‑data staging directory

# Step 5) Define filenames (logical names, not full paths yet)
# Expression
EXPR_FILENAME="salmon.merged.gene_tpm.tsv"

# Fulgent sample/QC table
SAMPLE_INFO_FILENAME="fulgent_qc_samples.csv"

# Patient metadata
PATIENT_INFO_FILENAME="patient_metadata.tsv"

# IHC table (optional)
IHC_FILENAME="ihc_values.tsv"

# Mutations (directory with many MAF batches)
MAF_DIRNAME="wes_maf_batches"

# Step 6) Copy raw files into the project
cp /path/to/${EXPR_FILENAME}    ${DIR_NEW_PROJECT}/unformatted_files/

cp /path/to/${SAMPLE_INFO_FILENAME}    ${DIR_NEW_PROJECT}/unformatted_files/

cp /path/to/${PATIENT_INFO_FILENAME}    ${DIR_NEW_PROJECT}/unformatted_files/

# Optional
cp /path/to/${IHC_FILENAME}    ${DIR_NEW_PROJECT}/unformatted_files/

# MAF batches
cp -r /path/to/${MAF_DIRNAME}       ${DIR_NEW_PROJECT}/unformatted_files/




