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