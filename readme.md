# SwissMADE

The work of this project is described in our paper [here](https://www.overleaf.com/read/mgwzpcbmrtxc), which was published as part of ICPR 2021. This repository contains sample data and scripts used for this work.

## This repository

* `codes` contains ICD-10 codes as they pertain to the relevant diseases and diagnoses.
* `data` is not uploaded, as it, although all reports are anonymised, might contain sensitive patient information. It contains a sample of 400 reports that we're selected from 4 categories in their original `json` format, converted to `txt` and, manually annotated in `xml`.
* `forms` contains administrative paperwork used for this project, most importantly the DTA.
* `ksb` contains various files related to the extraction and conversion of data from KSB: most importantly the `dump...sql` (not uploaded), which contains the entire database.
* `schema` contains the GATE-compatible annotation schema.
* `scripts` contains various transformation and annotation scripts.



### Manually Annotated Subset

* Some reports have a structured section in which diagnoses are listed with their ICD-10 codes. These are not 100% reliable though. Still, we are using these to predict ADEs, focusing on 3 (4 if time permits) events: severe hemorage, pulmonary embolism, stroke (and AMI). For each of these, a set of 100 reports was created, taking as many positives as were found, and filling up the remaining positions with reports with for which no ADEs where predicted.

