import plotly.graph_objects as go
import plotly.colors

data = {
    'Travel': {
        'Activities': ['HikingProject', 'Viator', 'AllTrails', 'Komoot', 'Context Travel'],
        'Travel Guides': ['Expert Vagabond', 'Yelp', 'Nomadic Matt', 'Rough Guides', 'The Blonde Abroad', 'TripAdvisor', 'Trustpilot', 'Lonely Planet', 'Trip.com', 'The Points Guy'],
        'Booking': ['Skyscanner', 'Kayak', 'Booking.com', 'expedia.com', 'Hilton', 'Google Flights', 'Airbnb']
    },
    'Services': {
        'Government & Legal': ['LegalZoom', 'Nolo', 'FreeTaxUSA', 'National Institute of Standards and Technology', 'European Union Official Website', 'Avvo', 'DigiCert', 'MPSC', 'Australia.gov.au', 'DMV appointments', 'National Council', 'Rocket Lawyer', 'Canada.ca', 'Gov.uk', 'National Institutes of Health', 'USA.gov'],
        'Household': ['Houzz', 'Build.com', 'Con Edison', 'HomeAdvisor', 'Thumbtack', "Angie's List", 'TaskRabbit', 'Surgaz'],
        'Healthcare': ['Healthline', 'zocdoc.com', 'U.S. Military Health System', 'BetterDoctor', 'MedlinePlus', 'Duodopa'],
        'Transportation': ['Citymapper', 'UPS', 'Ola', 'Rome2rio']
    },
    'Information': {
        'Weather': ['USGS', 'NOAA', 'EMSC', 'WeatherBug', 'Earthquake Track', 'National Weather Service', 'OpenWeatherMap'],
        'Finance': ['MarketWatch', 'Reuters', 'The Economist', 'YNAB', 'Financial Times', 'Bloomberg', 'Investing.com', 'CNBC'],
        'Reference & Education': ['HowStuffWorks', 'JSTOR', 'Instructables', 'Udacity', 'ScienceDirect', 'Politechnika Morskaw Szczecinie', 'Britannica', 'WikiHow', 'arXiv', 'DoItYourself', 'edX', 'Wikipedia', 'Google Scholar', 'Udemy'],
        'News & Media': ['The Washington Post', 'The New York Times', 'Nextdoor', 'Apple News', 'CNN', 'The Guardian', 'Google News', 'BBC', 'Flipboard', 'Al Jazeera']
    },
    'Social': {
        'Communities & Forums': ['Indigo', 'Kickstarter', 'FindNovel', 'hackinthebox', 'Reddit'],
        'Social Media': ['TikTok', 'LinkedIn', 'Twitter', 'Instagram', 'Facebook', 'Pinterest'],
        'Communication Tools': ['Android', 'Gmail', 'Outlook', 'Deutsche Telekom', 'Skype']
    },
    'Entertainment': {
        'Tickets': ['Ticketmaster', 'eventbrite.com', 'Meetup', 'SeatGeek', 'Fandango', 'StubHub', 'Bandsintown'],
        'Streaming': ['Netflix', 'IVI Streaming Service', 'Apple TV', 'Amazon Music', 'Disney+', 'Apple Music', 'Tidal', 'Spotify', 'Hulu', 'Deezer'],
        'Gaming': ['Roblox', 'Itch.io', 'ESL Gaming', 'Battlefy', 'Steam', 'Twitch']
    },
    'Shopping': {
        'E-Commerce': ['Tower Electric Bikes', 'AliExpress', 'Redbubble', 'Rakuten', 'Walmart'],
        'Specialty Stores': ['Newegg', 'Uniqlo', 'Tire Rack', 'Zara', 'Samsung Checkout', 'Xiaomi', 'MIUI', 'RockAuto', 'ASOS', 'L.L Bean', 'Samsung', 'HP', 'Turbo Detail Models', 'H&M', 'Micro Center', 'NVIDIA', 'siigo memory', 'Dynamax', 'B&H Photo Video', 'DEX'],
        'Digital Products': ['Humble Bundle', 'Unity', 'Microsoft Store', 'SoundCloud', 'Epic Games Store', 'Autodesk', 'GOG', 'Audible']
    },
    'Work': {
        'Corporate Tools': ['Cloudflare', 'Google Drive', 'Microsoft Office', 'Dropbox', 'Microsoft Teams', 'Microsoft SharePoint', 'Slack', 'Microsoft Azure', 'Google Analytics', 'Namecheap', 'Bitly', 'Google DoubleClick', 'Gandi', 'DoubleVerify', 'Rubicon Project', 'Google Ads', 'F5', 'Asana', 'Trello'],
        'Employment': ['Fiverr', 'Upwork', 'Coursera', 'Indeed']
    },
    # 'Financial': {
    #     'Investment Platforms': ['Alpaka'],
    #     'Payment Gateways': ['Stripe', 'BMS.GROUP']
    # }
}

ids = []
labels = []
parents = []
values = []
hover_texts = []

total_websites = 0
domain_totals = {}
subdomain_counts = {}

for domain, sub_domains_dict in data.items():
    domain_total = 0
    ids.append(domain)
    labels.append(domain)
    parents.append("")
    values.append(0)

    for sub_domain, websites in sub_domains_dict.items():
        count = len(websites)
        domain_total += count
        total_websites += count
        sub_domain_id = f"{domain}/{sub_domain}"
        subdomain_counts[sub_domain_id] = count

        ids.append(sub_domain_id)
        labels.append(sub_domain)
        parents.append(domain)
        values.append(count)

    domain_totals[domain] = domain_total

final_hover_texts = []
for i in range(len(ids)):
    current_id = ids[i]
    current_label = labels[i]

    if current_id in domain_totals: # Domain
        domain_total = domain_totals[current_id]
        percentage = (domain_total / total_websites) * 100 if total_websites > 0 else 0
        final_hover_texts.append(f"<b>{current_label}</b><br>Total Count: {domain_total}<br>Overall: {percentage:.1f}%")
    elif current_id in subdomain_counts: # Sub-domain
         sub_domain_count = subdomain_counts[current_id]
         parent_domain = parents[i]
         parent_total = domain_totals[parent_domain]
         percent_of_parent = (sub_domain_count / parent_total) * 100 if parent_total > 0 else 0
         percent_of_root = (sub_domain_count / total_websites) * 100 if total_websites > 0 else 0
         final_hover_texts.append(f"<b>{current_label} ({parent_domain})</b><br>Count: {sub_domain_count}<br>% of {parent_domain}: {percent_of_parent:.1f}%<br>% of Total: {percent_of_root:.1f}%")
    else:
        final_hover_texts.append(current_label)


fig = go.Figure(go.Treemap(
    ids=ids,
    labels=labels,
    parents=parents,
    values=values,
    texttemplate="%{label} (%{percentRoot:.1%})",
    hoverinfo="text",
    hovertext=final_hover_texts,
    pathbar_textfont_size=115,
    root_color="lightgrey",
    textfont_size=15,
))

fig.update_layout(
    uniformtext=dict(minsize=10, mode='hide'),
    title_text='Website Distribution by Domain and Sub-domain',
    title_x=0.5,
    margin=dict(t=50, l=25, r=25, b=25),
    colorway=plotly.colors.qualitative.Plotly
)


fig.show()
