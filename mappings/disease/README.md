# Manual disease term mappings

This directory contains two large mapping files related to disease terms.

## String to ontology

Maps free text disease names (such as “Acheiropody”) to a EFO term (such as http://www.orpha.net/ORDO/Orphanet_931). The file is a 7 column format used by ZOOMA.

When amending the file manually, make sure to follow the format:
1. STUDY is the source from which the disease string originated.
2. BIOENTITY column is always blank.
3. PROPERTY_TYPE is always _disease._
4. PROPERTY_VALUE is the source disease name, such as _Acheiropody._
5. SEMANTIC_TAG is the target ontology term, such as http://www.orpha.net/ORDO/Orphanet_931. This should be a full URI and not a CURIE.
6. ANNOTATOR contains the names of people who worked on the term. If adding a new entry, use only your name. If updating an existing term, add your name (comma-and-space separated) to the rightmost position of the list.
7. ANNOTATION_DATE is the date when the mapping was last updated. The format is YYYY-MM-DD HH:MM:SS. The time portion doesn't have to be exact and can be filled with a placeholder 12:00:00.

For introducing the changes, the file could be imported into Google Sheets and exported back as TSV.

The maintenance script, `normalise.py`, reads the current manual mappings file (`manual_string.tsv`), performs certain normalisations (such as sorting and duplicate removal), and outputs the updated mappings as `efo/manual_string_NORM.tsv`. This file can then be inspected and moved to replace the original input file. To use the script, install dependencies: `pip install --upgrade pandas ontoma`.

## Ontology to ontology

The second file, `manual_xref.tsv`, is currently not used and only exists as a placeholder.
