# Curated input data for Open Targets Genetics


## GWAS Catalog study curation

This `.tsv` file contains list of GWAS Catalog study identifiers that have harmonised summary statistics with their manually/semi automatically assigned curated metadata eg. failed quality control or the QTL nature of the study. The format is tab separated values.

### Schema

- **studyId** - GCST study accession to identify study.
- **analysisFlag** - applied statistical method authors used that might have downstream implication in interpreting the associations discovered by the study.
- **studyType** - sometimes, curation required to override the automatic assumption of the type of a study. 
- **qualityControl** - annotation on issues that prevent the study from ingestion (eg. `failing summary statistics QC`).
- **isCurated** - boolean flag indicating if the study went through curation.