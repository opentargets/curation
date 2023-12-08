# Curated input data for OpenTargets Genetics


## GWAS Catalog study curation

This `.tsv` file contains list of GWAS Catalog study identifiers that have harmonised summary statistics with their manually/semi automatically assigned curated metadata eg. failed quality control or the QTL nature of the study. The format is tab separated values.

### Schema

- **studyId** - GCST study accession to identify study
- **analysisFlag** - comment on the applied statistical method authors used that might have downstream implication in our pipelines.
- **updateStudyType** - if a study is not really a GWAS, but a qtl. This string will be picked up and replace the `type` value in the study index.
- **qualityControls** - `|` separated list of identified issues that prevent the study from ingestion.
- **isCurated** - boolean flag indicating if the study went through curation.