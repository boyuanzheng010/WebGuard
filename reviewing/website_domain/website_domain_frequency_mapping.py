import pprint
from collections import defaultdict
import re
import pandas as pd
import json
from parsing_util import check_duplication, extract_website_to_domain_mapping, extract_domain_to_website_mapping
from parsing_util import extract_filename2website_mapping, classify_into_domains


def normalize(name: str) -> str:
    name = re.sub(r"[^\w\s]", "", name, flags=re.UNICODE)
    name = re.sub(r"\s+", "", name)
    name = re.sub(r"_", "", name)
    return name.strip().lower()


# Part 1: Parse Scale CB Meta Data
annotation_meata_file_path = "/Users/zheng.2372/PycharmProjects/web-monitor-neurips/reviewing/website_domain/data/Browser-Safety-Annotation-CB-meta.csv"
website_filename2name = extract_filename2website_mapping(annotation_meata_file_path)

# Part 2: Check Domain Classification
website_domain_file = '/Users/zheng.2372/PycharmProjects/web-monitor-neurips/reviewing/website_domain/data/website_selection.md'
duplicates = check_duplication(website_domain_file)
pprint.pprint(duplicates)
all_website2domain = extract_website_to_domain_mapping(website_domain_file)

# Part 3: Align website from filename to website name
all_website_list = ['Hiking Porject', 'legalzoom', 'HOUZZ', 'usgs', 'Indigo_nails', 'Expertvagabond', 'healtline',
                    'Tik_Tok', 'Marketwatch', 'reuters', 'howstuffworks', 'Jstor', 'Citymapper', 'SkyScanner',
                    'ticketmaster', 'towerelectricbikes', 'zocdoc', 'Cloudfare', 'Netflix', 'KAYAK', 'viator', 'Roblox',
                    'instructables', 'Alpaca', 'Kickstarter', 'Newegg', 'Yelp', 'fiverr', 'eventbrite', 'Findnovel',
                    'nomadicmatt', 'RoughGuides', 'Nolo', 'Uniqlo', 'washingtonpost', 'Google-drive', 'health mil',
                    'UDACITY', 'BOOKING', 'Office', 'Nytimes', 'tirerack', 'android', 'alltrails', 'FreetaxUSA',
                    'dropbox', 'expedia', 'Microsoft Teams', 'zara', 'nist gov', 'HUMBLEBUNDLE', 'sharepoint', 'hitb',
                    'The_Economist', 'theblondeabroad', 'MEETUP', 'Linkedin', 'twitter', 'ivi_ru', 'NOA', 'Upwork',
                    'Tripadvisor', 'itch', 'Samsung Checkout', 'AppleTV', 'sciencedirect', 'seatgeek', 'Gmail',
                    'Amazon_music', 'outlook', 'Slack', 'european_union', 'azure', 'emsc-csem', 'aliexpress', 'Xiaomi',
                    'Weather_Bug', 'STRIPE', 'UPS', 'eslgaming', 'MIUI', 'Build', 'ROCKAUTO', 'Ola cabs', 'avvo',
                    'YNAB', 'digicert', 'Instagram', 'am.szczecin.pl', 'Trustpilot', 'Analytics', 'Telekom',
                    'Namecheap', 'Nextdoor', 'asos', 'disneyplus', 'bitly', 'Apple music', 'rome2rio', 'coned',
                    'Facebook', 'Homeadvisor', 'Fandango', 'L.L.Bean', 'Financial_Times', 'Google DoubleClick', 'Unity',
                    'britannica', 'Apple_news', 'Thumbtack', 'mpsc.gov.in', 'CNN', 'Samsung', 'battlefy', 'TheGuardian',
                    'Australia gov au', 'DMV', 'StubHub', 'MICROSOFT', 'Soundcloud', 'komoot', 'National Council',
                    'WIKIHOW', 'gandi', 'Angieslist', 'Contexttravel', 'earthquaketrack', 'store.steampowered', 'HP',
                    'DoubleVerify', 'turbodetailmodels', 'bloomberg', 'WEATHER', 'Googlenews', 'hilton',
                    'openweathermap', 'bandsintown', 'TWITCH', 'hm', 'Tidal', 'arxiv', 'MicroCenter',
                    'Rubicon_Project_(Magnite)', 'taskrabbit', 'rocketlawyer', 'doityourself', 'BBC', 'edx',
                    'Wikipedia', 'investing', 'Nvidia', 'SPOTIFY', 'betterdoctor', 'lonelyplanet', 'Google Ads', 'f5',
                    'pinterest', 'GoogleScholar', 'EPIC', 'bmsgroup', 'Canadaca', 'Trip_com', 'Redbubble',
                    'siigo memory', 'Dynamax', 'rakuten', 'Surgaz.ru', 'bhphotovideo', 'Reddit project',
                    'Grand_nord_auto', 'FLIPBOARD', 'Coursera', 'THEPOINTSGUY', 'Hulu', 'Autodesk', 'Deezer',
                    'Google Flights', 'GOVUK', 'cnbc', 'asana', 'gog', 'Walmart', 'Udemy', 'Trello',
                    'National Institutes of Health', 'Airbnb', 'Usa_gov', 'Skype', 'audible', 'Medlineplus', 'INDEED',
                    'ALJAZEERA', 'duodopapatient']

# annotated_website2domain = {}
# for website_filename in all_website_list:
#     # Map website to domain
#     website_name = website_filename2name[website_filename.lower()][0]
#     url = website_filename2name[website_filename.lower()][1]
#     domains = all_website2domain[website_name]
#     annotated_website2domain[website_name] = domains
#
# annotated_domain2website = classify_into_domains(annotated_website2domain)
# # Save to file
# with open('/Users/zheng.2372/PycharmProjects/web-monitor-neurips/reviewing/website_domain/data/website2domain_mapping.json', 'w', encoding='utf-8') as f:
#     json.dump(annotated_domain2website, f, ensure_ascii=False, indent=4)

annotated_website2domain = {}
for website_filename in all_website_list:
    # Map website to domain
    website_name = website_filename2name[website_filename.lower()][0]
    url = website_filename2name[website_filename.lower()][1]
    domains = all_website2domain[website_name]
    annotated_website2domain[website_filename] = domains
annotated_domain2website = classify_into_domains(annotated_website2domain)

# Save to file
with open('/Users/zheng.2372/PycharmProjects/web-monitor-neurips/reviewing/website_domain/data/website2domain_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(annotated_website2domain, f, ensure_ascii=False, indent=4)

with open('/Users/zheng.2372/PycharmProjects/web-monitor-neurips/reviewing/website_domain/data/domain2website_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(annotated_domain2website, f, ensure_ascii=False, indent=4)


print()
