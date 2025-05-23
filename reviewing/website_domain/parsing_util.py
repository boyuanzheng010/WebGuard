from collections import defaultdict
import re
import pandas as pd

def check_duplication(file_path):
    # Find the duplication
    site_domains = defaultdict(set)

    current_high = None
    current_low = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('...'):
                continue
            if line.startswith('# ') and not line.startswith('##'):
                current_high = line[2:].strip()
                current_low = None
                continue
            if line.startswith('## '):
                current_low = line[3:].strip()
                continue
            if current_high and current_low:
                name = line
                site_domains[name].add((current_high, current_low))

    # filter out websites in more than one domain
    duplicates = {name: list(domains)
                for name, domains in site_domains.items()
                if len(domains) > 1}
    return duplicates


def extract_website_to_domain_mapping(file_path):
    results = {}
    current_high = None
    current_low = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines or ellipsis lines
            if not line or line.startswith('...'):
                continue
            # High-level domain heading: lines starting with single '# ' but not '##'
            if line.startswith('# '):
                # Ensure it's not '##'
                if not line.startswith('##'):
                    current_high = line[2:].strip()
                    current_low = None
                    continue
            # Low-level domain heading: lines starting with '## '
            if line.startswith('## '):
                current_low = line[3:].strip()
                continue
            # Otherwise, line is a website entry
            if current_high and current_low:
                name = line
                results[name] = [current_high, current_low]

    return results


def extract_domain_to_website_mapping(file_path):
    nested = defaultdict(lambda: defaultdict(list))

    current_high = None
    current_low = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('...'):
                continue
            if line.startswith('# ') and not line.startswith('##'):
                current_high = line[2:].strip()
                current_low = None
                continue
            if line.startswith('## '):
                current_low = line[3:].strip()
                continue
            if current_high and current_low:
                site = line
                nested[current_high][current_low].append(site)

    result = {high: dict(lows) for high, lows in nested.items()}

    return result

def extract_filename2website_mapping(file_path):
    df = pd.read_csv(file_path)
    rows_as_dicts = df.to_dict(orient="records")

    website_id2name = {}
    for item in rows_as_dicts:
        website_id2name[item['FILE_NAME'].replace('.zip', '').lower()] = [item['WEBSITE'], item['URL']]
    return website_id2name


def classify_into_domains(website2domain):
    new_structure = defaultdict(lambda: defaultdict(list))

    for website, (high_level, low_level) in website2domain.items():
        new_structure[high_level][low_level].append(website)

    def convert_defaultdict(d):
        if isinstance(d, defaultdict):
            d = {k: convert_defaultdict(v) for k, v in d.items()}
        return d

    new_structure = convert_defaultdict(new_structure)

    return new_structure




