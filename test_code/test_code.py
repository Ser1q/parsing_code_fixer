from bs4 import BeautifulSoup
import cloudscraper
import csv 
url = "http://localhost:8000/index_altered.html"

response = cloudscraper.create_scraper().get(url)

soup = BeautifulSoup(response.text, "html5lib")
print(soup.prettify)

properties = []

property_list = soup.find("div", class_="property-list")
# print(property_list)

property_cards = property_list.find_all("div", class_="property-card")

for card in property_cards:
    property = {}
    property["name"] = card.find("h3").text.split("\n")[1].strip()
    property["address"] = (
        card.find("p", class_="card-text").text.split("\n")[1].strip()
    )
    property["image"] = card.find("img").get("src")

    info = card.find_all("li", class_="card-item")
    property["bedrooms"] = info[0].span.text[:-5]
    property["bathrooms"] = info[1].span.text[:-6]
    property["area"] = info[2].span.text[:-5]

    properties.append(property)

with open('properties.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'address', 'price', 'image', 'bedrooms', 'bathrooms', 'area']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for property in properties:
        writer.writerow(property)