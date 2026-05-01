#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: setup_new_project.sh <PROJECT_NAME>"
  exit 1
fi

PROJECT_NAME="$1"

DIR_REPO="${HOME}/git/cbioportal_data_ingestion"
DIR_PROJECT_ROOT="${HOME}/projects/cbioportal_ingestion"
DIR_PROJECT="${DIR_PROJECT_ROOT}/${PROJECT_NAME}"

mkdir -p "${DIR_PROJECT}/config" \
         "${DIR_PROJECT}/unformatted_files" \
         "${DIR_PROJECT}/output" \
         "${DIR_PROJECT}/logs"

cp "${DIR_REPO}/templates/project_setup_parameters.txt" \
   "${DIR_PROJECT}/config/project_setup_parameters.txt"

cp "${DIR_REPO}/templates/run_ingestion.sh" \
   "${DIR_PROJECT}/run_ingestion.sh"

chmod +x "${DIR_PROJECT}/run_ingestion.sh"

echo "Created:"
echo "  ${DIR_PROJECT}/config/project_setup_parameters.txt  (EDIT THIS ONLY)"
echo "  ${DIR_PROJECT}/run_ingestion.sh                     (DO NOT EDIT)"
echo "Next: emacs ${DIR_PROJECT}/config/project_setup_parameters.txt"
