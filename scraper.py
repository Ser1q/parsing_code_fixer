import cloudscraper
from bs4 import BeautifulSoup, Comment
import time

def scrape_website(website): # getting raw html with cloudscraper
    print('Creating cloudscraper session...')
    # Create a cloudscraper instance with custom settings
    # delay=10 adds a delay between requests to avoid rate limiting
    # browser settings mimic a Chrome browser on Windows desktop
    scraper = cloudscraper.create_scraper(
        delay=10,
        browser={
            "browser": "chrome",
            "platform": "windows",
            "desktop": True
        }
    )

    try:
        print(f'Fetching {website} ...')
        response = scraper.get(website)
        time.sleep(5) 

        if response.status_code == 200:
            print('Page loaded successfully')
            return response.text
        else:
            print(f'Failed to load page: {response.status_code}')
            return None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def extract_body_content(html_content): # extracting body
    soup = BeautifulSoup(html_content, 'html5lib')
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ''

def clean_html_for_llm(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Remove scripts, styles, and invisible content
    for tag in soup(['script', 'style','ion-icon', 'button', 'noscript', 'svg', 'meta', 'link']):
        tag.decompose()

    # Optionally remove tags with display:none or hidden
    for tag in soup.find_all(style=lambda x: x and "display:none" in x):
        tag.decompose()

    
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
        
    return soup.prettify(formatter="minimal").replace("\n", "").replace("  ", "")

def split_dom_content(dom_content, max_size=6000):
    return [
        dom_content[i:i+max_size] for i in range(0, len(dom_content), max_size)
    ]