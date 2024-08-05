# URL of the website to scrape
base_url = "https://pubmed.ncbi.nlm.nih.gov/?term=%28%28Switzerland%5BAffiliation%5D%29+AND+%28fibroblasts%5BText+Word%5D%29%29+AND+%28cell+culture%5BText+Word%5D%29&sort="

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def fetch_html(url):
    #Fetch HTML content from the given URL.
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def parse_max_pages(soup):
    #Parse the maximum number of pages from the HTML content.
    """<input aria-label="page number input" class="page-number" data-ga-action="Jump_to_page_top" 
    data-ga-category="pagination" id="page-number-input" max="59" min="1" title="Press Enter to navigate to the page number." 
    type="number" value="1"></input>"""

    input_tag = soup.find('input', class_='page-number', id='page-number-input')
    if input_tag and 'max' in input_tag.attrs:
        return int(input_tag['max'])
    else:
        print("The max attribute was not found or the <input> tag does not exist.")
        return None

def extract_article_ids(soup):
    #Extract all article IDs from the given HTML content.
    """<a class="docsum-title" data-article-id="38821154" data-full-article-url="from_term=%28HPLC%5BText+Word%5D%29+AND+%28South+Korea%5BAffiliation%5D%29&amp;from_sort=date&amp;from_pos=1" 
    data-ga-action="1" data-ga-category="result_click" data-ga-label="38821154" href="/38821154/" ref="linksrc=docsum_link&amp;article_id=38821154&amp;ordinalpos=1&amp;page=1">
    Indole-3-acetic acid induced cardiogenesis impairment in in-vivo zebrafish via oxidative stress and downregulation of cardiac morphogenic factors.</a>"""
    
    a_tags = soup.find_all('a', attrs={'data-article-id': True})
    return [a_tag['data-article-id'] for a_tag in a_tags]

def scrape_all_pages(base_url, max_pages):
    #Scrape all pages for article IDs and return a list of all IDs.
    all_article_ids = []

    for page in range(1, max_pages + 1):
        page_url = f'{base_url}&page={page}'
        html_content = fetch_html(page_url)

        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            article_ids = extract_article_ids(soup)
            all_article_ids.extend(article_ids)
        else:
            print(f"Failed to retrieve page {page}")

    return all_article_ids
    
def extract_article_title(soup):
    #Extracts the article title
    return soup.title.string

def extract_authors_and_affiliations(soup):
    #Extract authors and their affiliations from the authors-list <div>.
    
    authors_list_div = soup.find('div', class_='authors-list')
    if not authors_list_div:
        print("Authors list not found.")
        return []

    authors = []
    author_spans = authors_list_div.find_all('span', class_='authors-list-item')

    for author_span in author_spans:
        author_name_tag = author_span.find('a', class_='full-name')
        author_name = author_name_tag.get_text(strip=True) if author_name_tag else "N/A"

        affiliation_links = author_span.find_all('a', class_='affiliation-link')
        affiliation_titles = [aff_link.get('title', 'N/A') for aff_link in affiliation_links]
        combined_affiliations = "; ".join(affiliation_titles)  # Combine with a semi-colon

        authors.append({
            'name': author_name,
            'affiliations': combined_affiliations
        })

    return authors

def extract_year(soup): 
    #Find the <span> with class 'date'
    year_span = soup.find('span', class_='date')
    if year_span:
        # Extract the text content
        year = year_span.text.strip()
        
        return year[0:4]
    else:
        return "N/A"
    
def extract_email(text):
    # Define a pattern that looks for email addresses after "Electronic address:" or similar strings
    pattern = r'(?:Electronic address:|Email:|e-mail:)\s*([\w\.-]+@[\w\.-]+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None
    
# Fetch the initial page content
initial_html = fetch_html(base_url)

if initial_html:
    initial_soup = BeautifulSoup(initial_html, 'html.parser')
    max_pages = parse_max_pages(initial_soup)

    if max_pages:
        # Scrape all pages for article IDs
        all_article_ids = scrape_all_pages(base_url, max_pages)
        print("Extracted Article IDs:", all_article_ids)

        with open(r'../data/raw/article_IDs.txt', 'w') as file:
            file.write('\n'.join(all_article_ids))
else:
    print("Failed to retrieve the initial page.")

with open(r'../data/raw/article_IDs.txt', 'r') as file:
    all_article_ids = file.read().split('\n')

database = [["ID", "Article Title", "URL", "Publication Year", "Author", "Affiliations"]]
for article in all_article_ids:
    url = f"https://pubmed.ncbi.nlm.nih.gov/{article}/"
    html_content = fetch_html(url)

    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')

        article_title = extract_article_title(soup)
        year = extract_year(soup)
        authors_data = extract_authors_and_affiliations(soup)
        for author in authors_data:
            author_details = [article, article_title.replace(" - PubMed", ""), url, year, author['name'], author['affiliations']]
            database.append(author_details)
            print(author_details)
    else:
        print("Failed to retrieve or parse the webpage.")

df = pd.DataFrame(database[1:], columns=database[0])
df.to_excel(r'../data/raw/authors_database.xlsx', index=False)

df = pd.read_excel(r'../data/raw/authors_database.xlsx')

df['Email Address'] = df['Affiliations'].astype(str).apply(lambda x: extract_email(x))
df.to_excel(r'../data/raw/authors_database_emails.xlsx', index=False)

df_filtered = df[df['Email Address'].notna() & (df['Email Address'] != '')]
df_remove_duplicate_email = df_filtered.drop_duplicates(subset='Email Address', keep="first")
df_remove_duplicate_email.to_excel(r'../data/processed/authors_database_emails.xlsx', index=False)