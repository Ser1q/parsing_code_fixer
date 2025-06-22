import cloudscraper
from bs4 import BeautifulSoup, Comment
import time
import json
import re
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

    
    
html = scrape_website("https://elite-motors.kz/ENG#rec771938267")
html_body = extract_body_content(html)
# with open("sandbox_products.html", "w", encoding="utf-8") as f:
#     f.write(html)

def parse_car_data(html_content):
    """
    Parse the Elite Motors HTML content and extract structured car rental data.
    Returns a list of dictionaries with car information.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    cars = []
    
    # The car data appears to be in elements with class 'tn-elem' containing car info
    # We'll look for elements that likely contain car information
    car_elements = soup.select('.tn-elem')
    
    for elem in car_elements:
        car = {}
        
        # Try to extract car name (this would need adjustment based on actual structure)
        name_elem = elem.select_one('.tn-atom[field*="name"]') or elem.select_one('.tn-atom[field*="title"]')
        if name_elem:
            car['name'] = name_elem.get_text(strip=True)
        
        # Try to extract price (looking for currency patterns)
        price_elem = elem.find(text=re.compile(r'\$\d+'))
        if price_elem:
            car['price'] = price_elem.strip()
        else:
            price_elem = elem.select_one('.tn-atom[field*="price"]')
            if price_elem:
                car['price'] = price_elem.get_text(strip=True)
        
        # Try to extract year (looking for 4-digit numbers that could be years)
        year_match = re.search(r'(20\d{2})', elem.get_text())
        if year_match:
            car['year'] = year_match.group(1)
        
        # Try to extract car image
        img_elem = elem.select_one('img.t-img')
        if img_elem and 'data-original' in img_elem.attrs:
            car['image_url'] = img_elem['data-original']
        
        # Try to extract specifications (this would need to be adjusted based on actual structure)
        spec_elems = elem.select('.tn-atom[field*="spec"]')
        if spec_elems:
            car['specifications'] = [spec.get_text(strip=True) for spec in spec_elems]
        
        # Only add to results if we found at least a name and price
        if car.get('name') and car.get('price'):
            cars.append(car)
    
    return cars




car_data = parse_car_data(html_body)

# Print the parsed data in a readable format
print("Found {} cars:".format(len(car_data)))
for i, car in enumerate(car_data, 1):
    print(f"\nCar #{i}:")
    for key, value in car.items():
        print(f"{key.title()}: {value}")

# Optionally save to JSON
with open('car_data.json', 'w', encoding='utf-8') as f:
    json.dump(car_data, f, ensure_ascii=False, indent=2)