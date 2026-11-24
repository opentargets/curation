# Curated input data for Open Targets Genetics


## GWAS Catalog study curation

This `.tsv` file contains list of GWAS Catalog study identifiers that have harmonised summary statistics with their manually/semi automatically assigned curated metadata eg. failed quality control or the QTL nature of the study. The format is tab separated values.

### Schema

- **studyId** - GCST study accession to identify study.
- **analysisFlag** - applied statistical method authors used that might have downstream implication in interpreting the associations discovered by the study.
- **studyType** - sometimes, curation required to override the automatic assumption of the type of a study. 
- **qualityControl** - annotation on issues that prevent the study from ingestion (eg. `failing summary statistics QC`).
- **isCurated** - boolean flag indicating if the study went through curation.


## Superseded studies

`superseded_studies.tsv` lists studies that another study supersedes, with the study that supersedes each one. The Open Targets pipeline drops a listed study only when the study that supersedes it is in the same run and passes study validation; otherwise it keeps the listed study.

It lists the GWAS Catalog studies that Psychiatric Genomics Consortium (PGC) fine-mapping supersedes ([opentargets/issues#4580](https://github.com/opentargets/issues/issues/4580)). PGC is a PPP source, so only the PPP run reads this file.

### Schema

- **studyId** - identifier of the superseded study (GCST accession).
- **supersededBy** - identifier of the study that supersedes it.


## scE2G biosample curation

`scE2G_biosample_mapping.csv` contains mappings of 60 scE2G Multiome prediction files listed in Supplementary Table S6 of Sheth et al. (2026).

*cell population* means a group of cells analysed together.
The groups range from all cells in a sample, through broad cell supergroups, to an individual annotated cell type.

### Schema

- **cellTypeId** - `cell_type_id` from Supplementary Table S6.
- **biosampleNameFromSource** - `cell_type_name` from Supplementary Table S6.
- **biosampleId** - id from biosampleIndex that match `biosampleName`.
- **biosampleName** - name of the matched BiosampleIndex id.
- **confidence** - confidence in the mapping: `High`, `Good`, or `Medium`.
- **cellPopulationLevel** - how the analysed cells were grouped: `allCells`
  for the full sample, `supergroup` for a broad cell lineage, or `cellType`
  for an annotated cell type. This field does not describe participant ancestry. This information is
  extracted from `cell_type_name` field.
- **tissueName** - tissue context, where one is available.
- **tissueId** - matching ontology ID for the tissue.

`tissueName` and `tissueId` are derived from Supplementary Table S6 `dataset`, `cell_type_id`, and `cell_type_name` fields and unified to biosampleIndex (only when feasible).

| Table S6 dataset family | Curated tissue | BiosampleIndex ID |
|---|---|---|
| `BMMC5`, `BMMC22`, `BMMC*_all` | bone marrow | `UBERON_0002371` |
| `PBMC5`, `PBMC9`, `PBMC*_all` | blood | `UBERON_0000178` |
| `islets`, `islets_all` | pancreas | `UBERON_0001264` |
| K562, GM12878, WTC11, HCT116, Jurkat datasets | blank | blank |


Three mappings warrant additional explanation:

- `Normoblasts` maps to `erythroblast` (`CL_0000765`), which lists
  `normoblast` as an exact synonym in the ontology. This is a `High`
  confidence match.
- `Pancreatic immune cells` maps to `leukocyte` (`CL_0000738`), which lists
  `immune cell` as an exact synonym. This is also a `High` confidence
  match; the tissue context is retained separately via `tissueName`/`tissueId`.
- `ID2-high myeloid progenitors` maps to the broader
  `myeloid lineage restricted progenitor cell` (`CL_0000839`). No CL term
  encodes the ID2-high marker used by this paper's clustering, so this
  mapping is a genuine rollup to the closest parent term and keeps
  `Medium` confidence.
