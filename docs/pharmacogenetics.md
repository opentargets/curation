# Extraction of observed phenotypes from pharmacogenetics studies

## PharmGKB phenotypes

[PharmGKB](https://www.pharmgkb.org/)'s clinical annotations consist of manually curated relationships between genetic variants and phenotypes. These annotations are based on the literature and are used to guide clinical decision making. The phenotypes are often described in free text and are not always easy to use programmatically.

PharmGKB provides a concise phenotype that is related to the genotype description, but this is often not enough to understand the full context of the relationship. We have used [OpenAI's text generation endpoint](https://platform.openai.com/docs/guides/text-generation) to parse the `genotypeAnnotationText` and generate a richer representation of the phenotype. A sample of the parsed phenotypes vs the original ones can be found in [this spreadsheet](https://docs.google.com/spreadsheets/d/1sAMTibza1K9LExVH8N-rZO1uue8koWbW9j5T3HpkhZs/edit?usp=sharing).
This is meant to overwrite the `phenotypeText` field in the original dataset.

This `.json` file contains list of ~15,000 genotype/phenotype relationships from the PharmGKB clinical annotations dataset. __Extracting all phenotypes takes ~7hours and ~12$, that is why we want to store parsed phenotypes in a file.__

### Schema

- **genotypeAnnotationText** - Text that accompanies the genotype annotation curated by PharmGKB. This is a free text field that can contain information about the genotype-phenotype relationship, the strength of the evidence, and the clinical implications of the relationship. 
- **phenotypeText** - List of texts that describe the genotype-phenotype relationship in a more concise and easier to interpret format. This text is parsed from `genotypeAnnotationText` using OpenAI's text generation endpoint.

### Updating the lookup

The pts `pharmacogenetics` step reads `pgx_phenotypes.json` and warns about ClinPGx texts missing from it. Whenever the pis `clinpgx_version` changes, run [`pharmacogenetics/extract_phenotypes.py`](../pharmacogenetics/extract_phenotypes.py) before tagging this repository, and open a PR with the updated file:

```sh
export OPENAI_API_KEY=...
uv run pharmacogenetics/extract_phenotypes.py \
    --clinpgx gs://otar012-eva/pharmacogenomics/cttv012-<clinpgx_version>.json.gz
```

The script finds the distinct `genotypeAnnotationText` values not yet in the lookup, parses only those with the same prompt and model as pts, and appends them without touching existing entries. A text already in the lookup counts as parsed even if its `phenotypeText` is empty. Texts whose extraction fails are listed and not written, so the next run retries them. Use `--dry-run` to list the missing texts without calling OpenAI, and `--texts unparsed_texts.json` to parse a JSON list of texts instead of a ClinPGx file.
