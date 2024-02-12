import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import random

def extract_article_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title and subtitle
        header = soup.find('header', class_='article-header')
        title = header.find('h1').get_text(strip=True) if header and header.find('h1') else 'Title Not Found'
        subtitle = header.find('p', class_='article__subhead').get_text(strip=True) if header and header.find('p', class_='article__subhead') else ''

        # Extract all text content
        content_div = soup.find('div', class_='wysiwyg wysiwyg--all-content css-ibbk12')
        paragraphs = content_div.find_all('p') if content_div else []
        content = ' '.join([p.get_text(strip=True) for p in paragraphs])

        return title, subtitle, content
    except Exception as e:
        print(f"Error extracting article from {url}: {e}")
        return 'Error', 'Error', 'Error'

def read_urls_and_extract_data(csv_input_path, csv_output_path):
    with open(csv_input_path, mode='r', newline='', encoding='utf-8') as infile, \
         open(csv_output_path, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)
        writer.writerow(['Title', 'Subtitle', 'Content', 'URL'])

        base_url = "https://www.aljazeera.com"
        urls = [row['Link'] for row in reader if row['Link'].startswith('/news/')]

        for url in tqdm(urls, desc="Processing articles"):
            full_url = base_url + url
            title, subtitle, content = extract_article_details(full_url)
            
            if title == 'Error' and subtitle == 'Error' and content == 'Error':
                print(f"Error occurred while processing article {full_url}")
            elif not content:
                print(f"No text found for article {full_url}")
            else:
                writer.writerow([title, subtitle, content, full_url])
            
            # Wait a random amount of time between 1 and 5 seconds
            time.sleep(random.randint(1, 5))

# Define your input and output CSV file paths
csv_input_path = 'articlesLinks.csv'  # This should be the path to your input CSV file
csv_output_path = 'articlesContent.csv'  # This will be the new CSV file with extracted details

read_urls_and_extract_data(csv_input_path, csv_output_path)
