## Mappings

Label to ontology mappings of different nature:
  - .
    - Labels of anatomical structures such as tissues, organs or systems are mapped to the [UBERON ontology](https://uberon.github.io).
    - Labels of cell lines are mapped to the [Cell Line Ontology](http://www.clo-ontology.org).
  - 


## Biosystems mappings

[biosystem](../mappings/biosystem) contains tissue, organ labels mappings to [UBERON](https://www.ebi.ac.uk/ols4/ontologies/uberon); labels to cell lines to [Cell-line ontology](https://www.ebi.ac.uk/ols4/ontologies/clo). 

### DepMap/Cell Model Passport mappings

`depmap_uberon_mappings.csv` - This file contains mapping of disease cell lines from [DepMap](https://depmap.org/portal/) and Sanger's [Cell Model Passport](https://cellmodelpassports.sanger.ac.uk/) dataset to the originating tissue. The mapping is done partially by automatic processes, then a manual curation step was applied to finalise the mappings.

**Schema:**

```
root
 |-- tissueFromSource: string (nullable = true)
 |-- tissueId: string (nullable = true)
 |-- tissueName: string (nullable = true)
```

Where `tissueFromSource` is an all-lower case label for the tissue as represented at the source. `tissueId` is the short form of mapped uberon or CLO identifier. `tissueName` is the label of the mapped term at the ontology.


## Disease mappings

[disease](../mappings/disease). Labels of diseases mapped to the [EFO ontology](https://www.ebi.ac.uk/efo/). This directory is pending to be harmonised under a common file (see [#1400](https://github.com/opentargets/platform/issues/1400) for context).