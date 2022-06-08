import os

import pandas as pd

from ontoma import ontology, owl


def count_and_save_mappings(mappings, filename):
    output_filename = os.path.join('efo', filename)
    mappings.to_csv(output_filename, sep='\t', index=False)
    return f'{len(mappings)} [{output_filename}]'


# Download and read EFO files.
owl.preprocess_owl('efo', 'latest')
efo_terms = pd.read_table('efo/terms.tsv')

# Count all mappings that we have to start with.
mappings = pd.read_table('manual_string.tsv')
print(f'Total: {count_and_save_mappings(mappings, "0_all.tsv")}')

# Get rid of leading/trailing whitespaces in place.
mappings['SEMANTIC_TAG'] = mappings['SEMANTIC_TAG'].str.strip()

# If there are any mappings where we cannot parse the target (EFO/other term), count and output them.
mappings['normalised_id'] = mappings['SEMANTIC_TAG'].apply(ontology.normalise_ontology_identifier)
no_semantic_tag = mappings[mappings['normalised_id'].isna()]
print(f'  Mapping target cannot be parsed: {count_and_save_mappings(no_semantic_tag, "1a_cannot_parse_mapping.tsv")}')
print(f'  Mapping target can be parsed: {len(mappings) - len(no_semantic_tag)}')

# Remove duplicates, keeping only the most recent annotation.
mappings['normalised_string'] = mappings['PROPERTY_VALUE'].str.lower()
before_deduplication_count = len(mappings)
mappings = (
    mappings
    .sort_values('ANNOTATION_DATE', ascending=False)
    .groupby(by=['normalised_string', 'normalised_id'])
    .first()
)
print(f'    Duplicates: {before_deduplication_count - len(mappings)} (removed)')
print(f'    Unique: {count_and_save_mappings(mappings, "2_unique.tsv")}')

# Analyse the EFO inclusion status.
mappings = mappings.merge(efo_terms, on='normalised_id', how='left', left_index=False, right_index=False)
print(f'      Not in EFO: {count_and_save_mappings(mappings[mappings["is_obsolete"].isna()], "3a_not_in_efo.tsv")}')
print(f'      In EFO but obsolete: {count_and_save_mappings(mappings[mappings["is_obsolete"] == True], "3b_obsolete.tsv")}')
print(f'      In EFO and live (current): {count_and_save_mappings(mappings[mappings["is_obsolete"] == False], "3c_live.tsv")}')

# Remove the extra columns and output the normalised dataframe.
mappings = mappings[['STUDY', 'BIOENTITY', 'PROPERTY_TYPE', 'PROPERTY_VALUE', 'SEMANTIC_TAG', 'ANNOTATOR', 'ANNOTATION_DATE']]
print(f'\nTotal mappings after normalisation: {count_and_save_mappings(mappings, "manual_string_NORM.tsv")}')
