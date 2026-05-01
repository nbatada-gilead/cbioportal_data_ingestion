    README.txt
    ==========
    Nizar Batada

    Reusable cBioPortal Data Ingestion Pipeline
    ============================================

    This repository supports a fully parameterized, reusable pipeline
    for preparing, validating, and loading clinical trial data into cBioPortal.

    Once set up, **no scripts need to be modified per study**.
    Only a single configuration file is edited for each new project.

    ------------------------------------------------------------
    PREREQUISITES 
    ------------------------------------------------------------

    1. Clone the pipeline repository:

       git clone ~/git/cbioportal_data_ingestion

    2. Ensure Python (with required packages) is available.
       Scripts assume Python >=3.9.

    3. Clone the validator (only once):

       git clone https://github.com/cBioPortal/datahub-study-curation-tools.git \
         ~/git/datahub-study-curation-tools

    ------------------------------------------------------------
    DIRECTORY CONVENTIONS
    ------------------------------------------------------------

    All projects live under:

      ~/projects/cbioportal_ingestion/

    Each project follows this structure (created automatically):

      <PROJECT_NAME>/
      ├── config/
      │   └── project_setup_parameters.txt   <-- ONLY file you edit
      ├── unformatted_files/
      │   ├── clinical/
      │   ├── rnaseq/
      │   ├── wes/
      │   └── ihc/
      ├── output/
      ├── logs/
      └── run_ingestion.sh                   <-- DO NOT EDIT

    All reusable scripts live in:

      ~/git/cbioportal_data_ingestion/scripts/

    ------------------------------------------------------------
    CREATING A NEW PROJECT
    ------------------------------------------------------------

    Step 1 — Create project skeleton
    --------------------------------

    Run (once per project):

      ~/git/cbioportal_data_ingestion/setup_new_project.sh <PROJECT_NAME>

    Example:

      ~/git/cbioportal_data_ingestion/setup_new_project.sh lung_translational

    This creates:
      - project directories
      - config/project_setup_parameters.txt
      - run_ingestion.sh

    ------------------------------------------------------------
    Step 2 — Edit project parameters (ONLY REQUIRED EDIT)
    ------------------------------------------------------------

    Open:

      emacs ~/projects/cbioportal_ingestion/<PROJECT_NAME>/config/project_setup_parameters.txt

    Fill in:

    - PROJECT_NAME
    - TYPE_OF_CANCER
    - REFERENCE_GENOME
    - STUDY_NAME
    - STUDY_DESCRIPTION

    Set data presence flags:
    - HAS_RNASEQ (true/false)
    - HAS_WES (true/false)
    - HAS_IHC (true/false)

    Provide input file paths relative to `unformatted_files/`.

    Nothing else needs to be edited.

    ------------------------------------------------------------
    Step 3 — Stage raw input data
    ------------------------------------------------------------

    Copy raw files into the appropriate subfolders, e.g.:

      unformatted_files/clinical/
      unformatted_files/rnaseq/
      unformatted_files/wes/
      unformatted_files/ihc/

    File names and paths must match those specified
    in project_setup_parameters.txt.

    ------------------------------------------------------------
    RUNNING THE PIPELINE
    ------------------------------------------------------------

    From the project directory:

      cd ~/projects/cbioportal_ingestion/<PROJECT_NAME>
      ./run_ingestion.sh

    ------------------------------------------------------------
    WHAT THE PIPELINE DOES (IN ORDER)
    ------------------------------------------------------------

    1. Harmonizes sample identifiers
    2. Adds WES samples (if enabled)
    3. Processes RNA-seq (optional):
       - Expression ID reconciliation
       - HUGO symbol enforcement
       - Z-score calculation
    4. Builds clinical tables:
       - data_clinical_patient.txt
       - data_clinical_sample.txt
    5. Processes IHC (optional):
       - Builds IHC clinical table
       - Merges into sample clinical file
    6. Builds mutation data from per-sample MAFs (optional)
    7. Generates case lists
    8. Writes all meta files
    9. Runs cBioPortal validator (if enabled)

    All outputs are placed under:

      output/

    Logs are written to:

      logs/pipeline.log

    ------------------------------------------------------------
    IMPORTANT RULES
    ------------------------------------------------------------

    - Do NOT edit run_ingestion.sh
    - Do NOT edit Python scripts
    - Do NOT manually edit meta files
    - Only edit:
        config/project_setup_parameters.txt
    - Only stage new raw data under unformatted_files/

    ------------------------------------------------------------
    ADDING NEW DATA TYPES
    ------------------------------------------------------------

    To add support for a new modality (e.g. protein, CNV):
    - Add a new HAS_* flag
    - Add ONE isolated block in run_ingestion.sh
    - Keep all logic in scripts/, never inline bash hacks

    ------------------------------------------------------------
    TROUBLESHOOTING
    ------------------------------------------------------------

    - Validation errors:
      Inspect logs/pipeline.log and output/* files.
    - SAMPLE_ID errors:
      Ensure IDs match across clinical, expression, WES, and IHC.
    - UTF-8 issues:
      Always regenerate mutation files from per-sample MAFs.

    ------------------------------------------------------------
    DESIGN PHILOSOPHY
    ------------------------------------------------------------

    - One config file per project
    - Deterministic, restartable steps
    - cBioPortal compliance by construction
    - No manual fixes after validation

    If you follow this structure, the same pipeline can be reused
    for ALL future clinical trials with minimal effort.
