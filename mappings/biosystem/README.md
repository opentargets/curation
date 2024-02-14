# Biosystems mappings

These files contains mappings to [UBERON](https://www.ebi.ac.uk/ols4/ontologies/uberon) or [Cell-line ontologies](https://www.ebi.ac.uk/ols4/ontologies/clo). 

- `depmap_uberon_mappings.csv` - This file contains mapping of disease cell lines from [DepMap](https://depmap.org/portal/) and Sanger's [Cell Model Passport](https://cellmodelpassports.sanger.ac.uk/) dataset to the originating tissue. The mapping is done partially by automatic processes, then a manual curation step was applied to finalise the mappings.

**Schema:**

```
root
 |-- tissueFromSource: string (nullable = true)
 |-- tissueId: string (nullable = true)
 |-- tissueName: string (nullable = true)
```

Where `tissueFromSource` is an all-lower case label for the tissue as represented at the source. `tissueId` is the short form of mapped uberon or CLO identifier. `tissueName` is the label of the mapped term at the ontology.