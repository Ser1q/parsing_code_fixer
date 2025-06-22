from smolagents import tool
import cloudscraper
import time
from bs4 import BeautifulSoup, Comment

@tool
def scrape_website(website: str) -> str: # getting raw html with cloudscraper
    """
    Scrapes the raw HTML content of a given website URL using a headless browser-like session.

    This function uses `cloudscraper` to bypass anti-bot protections (like Cloudflare)
    and retrieve the full HTML source code of the provided website. It simulates a real browser 
    (Chrome on Windows) to avoid detection, and introduces delay to reduce the chance of rate-limiting.

    Args:
        website (str): A full URL (including http/https) of the website to scrape.

    Returns:
        str: The raw HTML content of the page if successful; otherwise, returns None.

    Example:
        >>> scrape_website("https://example.com")
        '<html>...</html>'

    Notes:
        - A delay of 10 seconds is added between requests for safety.
        - The function handles exceptions and prints errors to console.
        - Ensure the input is a valid and reachable URL.

    Tools Used:
        - cloudscraper (to bypass protections like Cloudflare)
        - time.sleep (to delay requests for ethical scraping)
    """
    
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


@tool
def extract_body_content(html_content: str) -> str:
    """
    Extracts the <body> tag content from raw HTML input.

    Args:
        html_content (str): The full HTML document as a string.

    Returns:
        str: The content inside the <body> tag. If no <body> is found, returns an empty string.

    Example:
        >>> extract_body_content("<html><body><p>Hello</p></body></html>")
        '<body><p>Hello</p></body>'
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ''

@tool
def clean_html_for_llm(html: str) -> str:
    """
    Cleans raw HTML for LLM input by removing unnecessary or noisy tags and comments.

    Args:
        html (str): HTML content (full document or <body> section).

    Returns:
        str: Cleaned HTML with scripts, styles, hidden content, and comments removed.

    Steps:
    - Removes <script>, <style>, <svg>, <button>, <noscript>, and similar tags.
    - Strips out tags with display:none style.
    - Removes HTML comments.
    - Returns the prettified HTML as a compact string.

    Example:
        >>> clean_html_for_llm('<body><script>alert("x")</script><p>Keep this</p></body>')
        '<body><p>Keep this</p></body>'
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Remove unwanted tags
    for tag in soup(['script', 'style', 'ion-icon', 'button', 'noscript', 'svg', 'meta', 'link']):
        tag.decompose()

    # Remove elements with display: none
    for tag in soup.find_all(style=lambda x: x and "display:none" in x):
        tag.decompose()

    # Remove HTML comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    cleaned = soup.prettify(formatter="minimal").replace("\n", "").replace("  ", "")
    return cleaned