from bs4 import BeautifulSoup
import csv
from tqdm import tqdm

def extract_articles_and_save_to_csv(html_file_path, csv_file_path):
    # Load the HTML content from the local file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all articles with the specified class
    articles = soup.find_all('article', class_='gc u-clickable-card gc--type-post gc--list gc--with-image')
    
    # Open a CSV file to write the articles' data
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Title', 'Link', 'Published Date', 'Excerpt', 'Image URL'])
        
        # Use tqdm to show progress
        for article in tqdm(articles, desc="Extracting articles"):
            # Extract the title
            title = article.find('h3', class_='gc__title').get_text(strip=True)
            # Extract the link
            link = article.find('a', class_='u-clickable-card__link')['href']
            # Extract the published date
            published_date = article.find('span', class_='screen-reader-text').get_text(strip=True).replace('Published On ', '')
            # Extract the excerpt
            excerpt = article.find('p').get_text(strip=True) if article.find('p') else 'No excerpt'
            # Extract the image URL
            img_url = article.find('img', class_='gc__image')['src'] if article.find('img', class_='gc__image') else 'No image URL'
            
            # Write the article's data to the CSV file
            writer.writerow([title, link, published_date, excerpt, img_url])

# Path to your HTML file
html_file_path = './aljazeera_ukraine.html'
# Path where you want to save the CSV file
csv_file_path = './articlesLinks.csv'

# Run the function
extract_articles_and_save_to_csv(html_file_path, csv_file_path)
