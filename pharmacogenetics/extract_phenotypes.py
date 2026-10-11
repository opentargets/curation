# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "openai==3.2.0",
#     "fsspec[gcs]",
# ]
# ///
"""Extract phenotypes for ClinPGx annotation texts missing from `pgx_phenotypes.json`.

Run it whenever the pis `clinpgx_version` changes, before tagging this repository. It reads the
distinct `genotypeAnnotationText` values of a ClinPGx release, parses only those absent from the
lookup with OpenAI, and appends them to the lookup. Existing entries are never modified and the
file keeps its formatting, so the diff shows only the new records.

A text in the lookup counts as parsed even if its `phenotypeText` is empty: an empty extraction
is a valid answer. A text whose extraction fails (API error, unexpected response) is reported and
not written, so the next run retries it.

Usage:
    export OPENAI_API_KEY=...
    uv run pharmacogenetics/extract_phenotypes.py \\
        --clinpgx gs://otar012-eva/pharmacogenomics/cttv012-<clinpgx_version>.json.gz
    uv run pharmacogenetics/extract_phenotypes.py --clinpgx <file> --dry-run
    uv run pharmacogenetics/extract_phenotypes.py --texts unparsed_texts.json
"""

import argparse
import json
import logging
import os
import sys
import time
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import fsspec
from openai import OpenAI, OpenAIError

GPT_MODEL = 'gpt-5-nano-2025-08-07'
DEFAULT_LOOKUP = Path(__file__).parent / 'pgx_phenotypes.json'

logger = logging.getLogger('extract_phenotypes')


def read_clinpgx_texts(uri: str) -> set[str]:
    """Distinct `genotypeAnnotationText` values in a ClinPGx JSON lines file (local or gs://, gzipped or not)."""
    texts = set()
    with fsspec.open(uri, 'rt', compression='infer', encoding='utf-8') as fh:
        for line in fh:
            if line.strip():
                text = json.loads(line).get('genotypeAnnotationText')
                if text:
                    texts.add(text)
    return texts


def read_texts_list(uri: str) -> set[str]:
    """Texts from a JSON list of strings, such as the `unparsed_texts.json` written by pts."""
    with fsspec.open(uri, 'rt', compression='infer', encoding='utf-8') as fh:
        return {text for text in json.load(fh) if text}


def find_missing(texts: Iterable[str], lookup: list[dict]) -> list[str]:
    """Texts absent from the lookup, sorted so the appended records have a stable order."""
    parsed = {record['genotypeAnnotationText'] for record in lookup}
    return sorted(set(texts) - parsed)


def dump_lookup(lookup: list[dict]) -> str:
    """Serialise the lookup in the format of the committed file: compact, ASCII-escaped, no trailing newline."""
    return json.dumps(lookup, separators=(',', ':'))


def parse_phenotype_with_gpt(
    genotype_text: str, openai_client: OpenAI, gpt_model: str = GPT_MODEL
) -> list[str] | None:
    """Query the OpenAI API to extract the phenotype from the genotype text.

    Kept identical to `parse_phenotype_with_gpt` in the pts pharmacogenetics step, so extractions
    made here and those already in the lookup are consistent.
    """
    prompt = f"""
        Context: We want to analyse ClinPGx clinical annotations. Their data includes a column,"genotypeAnnotationText",
        which typically informs about efficacy,side effects, or patient response variability given a specific genotype.
        The data is presented in a lengthy and complex format, making it challenging to quickly grasp the key phenotypic
        outcomes.

        Aim: To parse the observed effect in a short string so that the effect can be easily interpreted at a glance.
        The goal is to extract the essence of the pharmacogenetic relationship. This extraction helps in summarizing the
        data for faster and more efficient analysis.

        Please analyse the following examples from the "genotypeAnnotationText" column and extract the key phenotype as
        a concise description. Format the result as a JSON array. Each JSON must only contain one field:
        "gptExtractedPhenotype".

        Examples for extraction:
        1. "Patients with the CTT/del genotype (one copy of the CFTR F508del variant) and cystic fibrosis may have "
           "increased response when treated with ivacaftor/tezacaftor combination as compared to patients with the "
           "CTT/CTT genotype." -> Expected extraction: "increased response"
        2. "Patients with the AC genotype may have "
           "increased risk for gastrointestinal toxicity with taxane and platinum regimens as compared to "
           "patients with the CC genotype." -> Expected extraction: "risk of gastrointestinal toxicity"
        3. "Patients with the rs2032582 AA genotype may be more likely to respond to tramadol "
           "treatment as compared to patients with the CC genotype." -> Expected extraction: "increased response"
        4. "Patients receiving methotrexate to treat acute lymphoblastic leukemia (ALL), and the "
           "rs4149056 TT genotype may be less likely to require glucarpidase treatment as compared to "
           "patients with the CC or CT genotypes." -> Expected extraction: "less likely to require glucarpidase"
        5. "Patients with the TT genotype and hormone insensitive breast cancer may experience "
           "increased risk of chemotherapy-induced amenorrhea when treated with goserelin or combinations of "
           "cyclophosphamide, docetaxel, doxorubicin, epirubicin, and fluorouracil compared to patients with the "
           "CT genotype." -> Expected extraction: "risk of chemotherapy-induced amenorrhea"
        6. "Patients with the GG genotype and cancer may have an increased risk for drug toxicity and an "
           "increased response to treatment with cisplatin or carboplatin as compared to patients with the AA or AG "
           "genotype. Other genetic and clinical factors may also influence a patient's risk for toxicity and "
           "response to platinum-based chemotherapy." -> Expected extraction: "drug toxicity" and "increased response"

        Based on these examples, please extract the phenotype from the following text:

        "{genotype_text}"
    """
    try:
        completion = openai_client.responses.create(
            model=gpt_model,
            text={'format': {'type': 'json_object'}},
            input=[
                {
                    'role': 'system',
                    'content': 'you are an expert in clinical pharmacology designed to output JSON.',
                },
                {'role': 'user', 'content': prompt},
            ],
            reasoning={'effort': 'minimal'},
        )
    except OpenAIError as e:
        logger.warning(f'{type(e).__name__} extracting phenotype, leaving it unparsed: {e}')
        return None
    try:
        generated_text = completion.output_text
        if not generated_text:
            logger.warning(f'No content generated for text: {genotype_text}')
            return None
        json_obj = json.loads(generated_text)
        if 'gptExtractedPhenotype' not in json_obj:
            # A missing key is a malformed answer, not an empty extraction: leave it out so it is retried.
            logger.warning(f'no gptExtractedPhenotype in the response for: {genotype_text[:80]}')
            return None
        return json_obj['gptExtractedPhenotype']
    except Exception as e:
        logger.error(f'Error parsing phenotype: {e}')
        return None


def parse_phenotypes(texts_to_parse: list[str], openai_client: OpenAI, max_workers: int = 10) -> dict[str, list[str]]:
    """Parse the phenotypes of the given texts concurrently; texts that fail are left out."""
    results_dict: dict[str, list[str]] = {}
    total = len(texts_to_parse)
    t_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_text = {
            executor.submit(parse_phenotype_with_gpt, text, openai_client): text for text in texts_to_parse
        }
        for i, future in enumerate(as_completed(future_to_text), 1):
            text = future_to_text[future]
            try:
                result = future.result()
            except Exception as e:
                logger.warning(f'{type(e).__name__} extracting phenotype, leaving it unparsed: {e}')
                result = None
            if isinstance(result, list):
                results_dict[text] = result
            elif isinstance(result, str):
                results_dict[text] = [result]
            if i % 50 == 0 or i == total:
                logger.info(f'progress {i}/{total}')
    logger.info(f'parsed {len(results_dict)}/{total} in {time.perf_counter() - t_start:.1f}s')
    return results_dict


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--clinpgx', help='ClinPGx annotation JSON lines file, local or gs://, optionally gzipped')
    source.add_argument('--texts', help='JSON list of texts to parse, such as unparsed_texts.json from pts')
    parser.add_argument('--lookup', default=str(DEFAULT_LOOKUP), help='phenotype lookup to update in place')
    parser.add_argument('--dry-run', action='store_true', help='list the missing texts without calling OpenAI')
    parser.add_argument('--concurrency', type=int, default=10, help='concurrent OpenAI requests')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    lookup_path = Path(args.lookup)
    lookup = json.loads(lookup_path.read_text(encoding='utf-8'))
    texts = read_clinpgx_texts(args.clinpgx) if args.clinpgx else read_texts_list(args.texts)
    missing = find_missing(texts, lookup)
    logger.info(f'{len(texts)} distinct texts, {len(missing)} missing from {lookup_path}')

    if args.dry_run or not missing:
        for text in missing:
            print(text)
        return 0

    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        logger.error('OPENAI_API_KEY is not set')
        return 2
    client = OpenAI(api_key=api_key, max_retries=2, timeout=30.0)
    parsed = parse_phenotypes(missing, client, max_workers=args.concurrency)

    lookup.extend({'genotypeAnnotationText': text, 'phenotypeText': parsed[text]} for text in missing if text in parsed)
    lookup_path.write_text(dump_lookup(lookup), encoding='utf-8')
    logger.info(f'appended {len(parsed)} records to {lookup_path}')

    failed = [text for text in missing if text not in parsed]
    if failed:
        logger.error(f'{len(failed)} texts failed and were not written; re-run to retry them:')
        for text in failed:
            print(text)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
