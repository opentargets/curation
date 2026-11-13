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

The 616 reports judged approved were given a disease in a second pass: `claude-opus-5-5` chose the disease that faithfully names TTD's text from text-search candidates, or answered `unmapped` for uses and catch-all categories ("radioactive tracer", "solid tumour/cancer"), and re-judged the mapped pair. 209 mappings are in `link_corrections.tsv`, each with a known disease id, confidence ≥ 0.8 and the mapped pair judged approved; the other 407 reports keep no disease.

### ChEMBL indication curation

[clinical/chembl](../clinical/chembl) corrects the diseases ChEMBL links to its indication references (`drug_indication` and `indication_refs`), which the Platform's `clinical_report` step turns into reports with provider `ChEMBL`. A ChEMBL report is one reference, such as a DailyMed label, an EMA product or an ATC code, and lists every disease ChEMBL links to it. A row here acts on one of those diseases and leaves the others alone.

#### `indication_corrections.tsv`

- `reportId`: the report id as the Platform publishes it. That is the DailyMed set id, the EMA product number or the ATC code as is, and a hash for INN, FDA and USAN references. Matching ignores case.
- `diseaseId`: the disease ChEMBL linked, as the report carries it, e.g. `MONDO_0002280`.
- `correctedDiseaseId`: either a disease id, which replaces `diseaseId` on that report, or `unmapped`, which removes the disease from the report. A report left with no disease is dropped. A disease id may be obsolete, as long as a current disease lists it in `obsoleteTerms`.
- `drugFromSource`, `diseaseFromSource`: ChEMBL's drug and disease names, for readability. They are not part of the key.
- `reason`: why the link is wrong and where the row comes from.

The key is `reportId` with `diseaseId`, and it must appear at most once. A row that matches no ChEMBL report is logged by the step and otherwise ignored.

The step applies these corrections before ChEMBL indications are used anywhere else, including as validation for the `UNVALIDATED_INDICATION` flag on trials.

**Schema:**

```
root
 |-- reportId: string
 |-- drugFromSource: string
 |-- diseaseFromSource: string
 |-- diseaseId: string
 |-- correctedDiseaseId: string
 |-- reason: string
```

#### How the 2026-11 rows were made

The rows cover ChEMBL indications that cite a DailyMed label. They were judged against the "Indications and Usage" section of the label itself (LOINC `34067-9`), fetched from DailyMed.

1. **First pass:** one label for each of the 4,294 drug–disease pairs in the 2612-2 inputs. `claude-opus-5-5` judged whether the label indicates the drug for the disease:
   - `indicated`;
   - `excluded`: only under Limitations of Use, "not indicated" and the like;
   - `not_indicated`: absent, or only context, a cause, a side effect or the population;
   - `unsure`.
2. **Second pass:** for each of the 512 pairs not judged `indicated`, every label that cites the pair was judged the same way (2,134 label–pair judgements).
3. **A disease is removed from a report only when its own label was judged `excluded` or `not_indicated` with confidence ≥ 0.8.** `unsure` verdicts and less confident ones leave the report as it is. A disease that another drug on the same report is indicated for is kept.

Result: 862 rows. 149 are limitations of use and 713 are uses the label doesn't give. Examples:
- Limitations of use: levoleucovorin → anemia, mecasermin → hypothyroidism, mesna → thrombocytopenia, icosapent ethyl → pancreatitis (opentargets/issues#4665).
- Uses the label doesn't give: ipratropium → asthma, ondansetron → cancer.

Eight rows replace the disease instead of removing it. These are drugs that would otherwise have lost every approved indication, and whose label clearly indicates another disease: conivaptan → hyponatremia, deferoxamine → iron poisoning, and buprenorphine and butorphanol → pain.

The judgements are not manually reviewed. Their `reason` gives the verdict, the confidence and the label words they rest on.
