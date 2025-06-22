from bs4 import BeautifulSoup
import re
import json


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

# Example usage:
if __name__ == "__main__":
    with open('./sandbox_products.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    car_data = parse_car_data(html_content)
    
    # Print the parsed data in a readable format
    print("Found {} cars:".format(len(car_data)))
    for i, car in enumerate(car_data, 1):
        print(f"\nCar #{i}:")
        for key, value in car.items():
            print(f"{key.title()}: {value}")
    
    # Optionally save to JSON
    with open('car_data.json', 'w', encoding='utf-8') as f:
        json.dump(car_data, f, ensure_ascii=False, indent=2)