# Extraction of observed phenotypes from pharmacogenetics studies

## PharmGKB phenotypes

[PharmGKB](https://www.pharmgkb.org/)'s clinical annotations consist of manually curated relationships between genetic variants and phenotypes. These annotations are based on the literature and are used to guide clinical decision making. The phenotypes are often described in free text and are not always easy to use programmatically.

PharmGKB provides a concise phenotype that is related to the genotype description, but this is often not enough to understand the full context of the relationship. We have used [OpenAI's text generation endpoint](https://platform.openai.com/docs/guides/text-generation) to parse the `genotypeAnnotationText` and generate a richer representation of the phenotype. A sample of the parsed phenotypes vs the original ones can be found in [this spreadsheet](https://docs.google.com/spreadsheets/d/1sAMTibza1K9LExVH8N-rZO1uue8koWbW9j5T3HpkhZs/edit?usp=sharing).
This is meant to overwrite the `phenotypeText` field in the original dataset.

This `.json` file contains list of ~15,000 genotype/phenotype relationships from the PharmGKB clinical annotations dataset. __Extracting all phenotypes takes ~7hours and ~12$, that is why we want to store parsed phenotypes in a file.__

### Schema

- **genotypeAnnotationText** - Text that accompanies the genotype annotation curated by PharmGKB. This is a free text field that can contain information about the genotype-phenotype relationship, the strength of the evidence, and the clinical implications of the relationship. 
- **phenotypeText** - List of texts that describe the genotype-phenotype relationship in a more concise and easier to interpret format. This text is parsed from `genotypeAnnotationText` using OpenAI's text generation endpoint.
