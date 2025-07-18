# SANTA for Historical NER

Fork of [S1s-Z/SANTA](https://github.com/S1s-Z/SANTA) with added datasets. Work in progress.

## Historical NER Instructions

### Datasets preparation
```bash
source scripts/prepare_hdsner.sh
```
- clones the datasets submodule
- creates the datasets conda environment
- downloads and pre-processes the datasets, with sequence length 64

### Environment setup
The conda environment used for the experiments is described in `environment.yml`.

### PLM download
```bash
python3 scripts/plm_download.py
```

### Format data and run model
```bash
bash scripts/run_hdsner.sh supervised # supervised setting
bash scripts/run_hdsner.sh distant # distantly-supervised setting
```
Results will be in `save/hdsner_DATASET-(supervised|distant)/`. \
**NOTE**: this will overwrite previous results of the same supervision method.

### Evaluate results
```bash
source scripts/eval_hdsner.sh
```
- activates the datasets environment
- evaluates results, writing to `dataset/hdsner_report_(dev|test).json`
- it contains both supervised and distant results, if previously run, in the same file

# Forked Readme

# SANTA

Hi, this is the code of our paper "SANTA: Separate Strategies for Inaccurate and Incomplete Annotation Noise in Distantly-Supervised Named Entity Recognition" accepted by ACL 2023 Findings. Our paper is available [here](https://arxiv.org/pdf/2305.04076.pdf).

## News:

Accepted by ACL 2023 Findings. 2023.05

Code released at Github. 2023.08

## Preparation
Download different pretrained LMs into resource/ 

Use environments.yaml to get the right environments

## Reproduce results
For Conll03:

>sh train_conll03.sh

For EC:

>sh train_EC.sh

For Webpage:

>sh train_NEWS.sh

For OntoNotes5.0:

>sh train_onto.sh

For BC5CDR:

>sh train_bc5cdr.sh

We got our results in single A40.
