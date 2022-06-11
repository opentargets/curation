# Open Targets curation repository

This repository contains a collection of different manual annotations produced within the [Open Targets organisation](https://www.opentargets.org).

## Content
- **Mappings**. Label to ontology mappings of different nature:
  - [biosystem](mappings/biosystem).
    - Labels of anatomical structures such as tissues, organs or systems are mapped to the [UBERON ontology](https://uberon.github.io).
    - Labels of cell lines are mapped to the [Cell Line Ontology](http://www.clo-ontology.org).
  - [disease](mappings/disease). Labels of diseases mapped to the [EFO ontology](https://www.ebi.ac.uk/efo/). This directory is pending to be harmonised under a common file (see [#1400](https://github.com/opentargets/platform/issues/1400) for context).

- **Target Safety annotation**. 
  Manual curation of experimental data and insights from publications and other well-known sources of target safety and toxicity data, including the Tox21 database.

  The annotation related to `safety_risks.tsv` and `adverse_effects.tsv` is currently being fed to the Platform's pipelines, whereas `experimental_toxicity.tsv` has been discontinued in favour of a new pipeline that processes [ToxCast data files](https://www.epa.gov/chemical-research/toxcast-data-accessing-toxcast-data-and-scenarios-exploring-data).

- **Gene Burden annotation**.
  Manual curation of burden tests from key publications and resources.

  - Schizophrenia Consortium. Associations of 9 genes with schizophrenia. The data is pulled from their downloads page (https://schema.broadinstitute.org/downloads).
  - Epi25 Consortium. Associations of 2 genes with epilepsy. The data is pulled from their downloads page (https://epi25.broadinstitute.org/downloads).
  - OTAR022 Metabolomics study. Associations of 21 genes with different metabolomics measurements. The data is pulled from 2 sites:
    - Table 1 of their manuscript provides the key metrics.
    - The sheet named "strongest gene/metabolite" in the Supplementary Table 5 provides annotation of nº samples.
  - CKD Publication. Associations of 3 genes with chronic kidney disease. The data is pulled from 2 sites:
    - Table 2 of their publication (https://jasn.asnjournals.org/content/jnephrol/30/6/1109.full.pdf?with-ds=yes).
    - Supplementary Table 5 provides annotation of nº samples.
  - Autism Sequencing Consortium. Associations of 102 genes with autism. The data is pulled from the Supplementary Table 2 in their publication (https://www.sciencedirect.com/science/article/pii/S0092867419313984#mmc2).
  - REGENERON. Associations of 497 genes with traits from the UK Biobank. The data has been parsed from the Supplementary Table 2, 3, and 4 of their publication (https://www.nature.com/articles/s41586-021-04103-z) + the mappings done by GWAS Catalog.