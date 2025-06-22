from bs4 import BeautifulSoup
import cloudscraper
import csv 
url = "http://localhost:8000/index_altered.html"

response = cloudscraper.create_scraper().get(url)

soup = BeautifulSoup(response.text, "html5lib")
print(soup.prettify)

properties = []

property_list = soup.find("div", class_="property-list")

property_cards = property_list.find_all("article", class_="property-card")

for card in property_cards:
    property = {}
    card_header = card.find("div", class_="card-header")
    property["name"] = card_header.find("h3", class_="card-title").get_text(strip=True)
    property["address"] = card.find("address", class_="property-address").get_text(strip=True)
    property["image"] = card.find("img", class_="property-image").get("src")
    price_data = card.find("data", class_="property-price")
    property["price"] = price_data["value"] if price_data and price_data.has_attr("value") else ""

    specs = card.find("ul", class_="property-specs").find_all("li", class_="property-spec")
    property["bedrooms"] = ""
    property["bathrooms"] = ""
    property["area"] = ""
    for spec in specs:
        data_tag = spec.find("data")
        label = spec.get_text(strip=True).lower()
        if "bed" in label:
            property["bedrooms"] = data_tag["value"] if data_tag and data_tag.has_attr("value") else ""
        elif "bath" in label:
            property["bathrooms"] = data_tag["value"] if data_tag and data_tag.has_attr("value") else ""
        elif "sqft" in label or "area" in label:
            property["area"] = data_tag["value"] if data_tag and data_tag.has_attr("value") else ""

    properties.append(property)

with open('properties.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'address', 'price', 'image', 'bedrooms', 'bathrooms', 'area']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for property in properties:
        writer.writerow(property)