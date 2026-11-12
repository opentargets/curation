## Clinical reports

### TTD curation

[clinical/ttd](../clinical/ttd) corrects rows of the [Therapeutic Target Database](https://ttd.idrblab.cn/) drug–disease file (`P1-05-Drug_disease.txt`) that the Platform's `clinical_report` step reads. Both files apply to TTD reports only, and are keyed on TTD's own drug id and indication text:

- `ttdDrugId`: the TTD drug id (`TTDDRUID`), e.g. `D0A001`.
- `diseaseFromSource`: the indication as TTD writes it. Matching ignores case.
- `drugFromSource`: TTD's drug name, for readability; it is not part of the key.
- `reason`: where the row comes from.

A key must appear at most once in each file. A row that matches no TTD report is logged by the step and otherwise ignored.

#### `stage_downgrades.tsv`

TTD rows labelled "Approved" for an indication no regulator has authorised the drug for. The report keeps its drug, disease and reference, but its clinical stage becomes `UNKNOWN`.

**Schema:**

```
root
 |-- ttdDrugId: string
 |-- drugFromSource: string
 |-- diseaseFromSource: string
 |-- reason: string
```

#### `link_corrections.tsv`

TTD rows whose drug or disease was matched to the wrong ChEMBL molecule or disease. For each side:

- an id (ChEMBL id, or an EFO/MONDO/HP/... disease id) replaces every id on that side of the report;
- `unmapped` removes the id from that side, so the report links nothing there;
- an empty cell leaves that side as the pipeline grounds it.

At least one of `drugId` and `diseaseId` must be filled. A disease id may be obsolete, as long as a current disease lists it in `obsoleteTerms`.

**Schema:**

```
root
 |-- ttdDrugId: string
 |-- drugFromSource: string
 |-- diseaseFromSource: string
 |-- drugId: string
 |-- diseaseId: string
 |-- reason: string
```

#### How the 2026-11 rows were made

Every TTD "Approved" pair in Platform 26.09 that no EMA, FDA, DailyMed or PMDA approval backs, for the same disease or a related one, was judged by `claude-opus-5-5` (1,702 pairs). The judge was checked on 100 regulator-approved and 100 never-approved control pairs. A second pass proposed replacements for the matches judged wrong.

The rows are not manually reviewed, and the rule is conservative: uncertain approvals are downgraded, and a link judged wrong without a confident replacement (confidence ≥ 0.8) is removed. See opentargets/issues#4662, #4665 and #4666.

A second set of 127 downgrades covers TTD "Approved" rows whose indication text could not be matched to a disease (for example "solid tumour/cancer" or "discovery agent"), which the first set left out. All 743 such reports in the 2612-2 inputs were judged by `claude-opus-5-5` on the drug and TTD's text alone. A report is downgraded unless every drug on it was judged approved with a faithful drug match. Of the 767 report–drug judgements, 122 were not approved, 4 unsure, and 12 approved but with the drug match judged wrong. These rows are not manually reviewed either. Their `reason` says "no mapped disease".
