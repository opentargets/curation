# Disease string-to-ontology and ontology-to-ontology mappings

The maintenance script, `normalise.py`, reads the current manual mappings file (`manual_string.tsv`), performs certain normalisations (such as sorting and duplicate removal), and outputs the updated mappings as `manual_string_NORM.tsv`. To use it, install dependencies: `pip install --upgrade pandas ontoma`.
