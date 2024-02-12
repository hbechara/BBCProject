from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime

# Function to check dates and find the earliest one
def find_earliest_date(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    date_divs = soup.find_all("div", class_="gc__date__date")
    earliest_date = None
    for div in date_divs:
        date_text = div.find("span", {"aria-hidden": "true"}).text
        article_date = datetime.strptime(date_text, "%d %b %Y")
        if not earliest_date or article_date < earliest_date:
            earliest_date = article_date
    return earliest_date

def run(playwright, specified_date_str):
    specified_date = datetime.strptime(specified_date_str, "%d %b %Y")
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.aljazeera.com/middle-east/")

    while True:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        page.wait_for_timeout(2000)
        
        html_content = page.content()
        earliest_date = find_earliest_date(html_content)
        if earliest_date:
            print(f"Earliest date found: {earliest_date.strftime('%d %b %Y')}")
            if earliest_date <= specified_date:
                print("Found a date lower than or equal to the specified. Stopping execution.")
                with open("aljazeera_middle_east.html", "w", encoding="utf-8") as file:
                    file.write(html_content)
                break
        
        if not page.is_visible("button.show-more-button.big-margin"):
            user_input = input("The 'Show more' button is not found. Try again? (y/n): ")
            if user_input.lower() != 'y':
                print("Stopping execution by user's choice.")
                break
            else:
                print("Attempting to find the 'Show more' button again...")
                page.wait_for_timeout(5000)  # Wait a bit longer before trying again
        else:
            page.click("button.show-more-button.big-margin")
            page.wait_for_timeout(5000)

    user_input = input("Done, press anything to finish... ") # This avoids force closing the browser
    browser.close()
    
with sync_playwright() as playwright:
    run(playwright, "6 Oct 2023") # Specify the date parameter here
