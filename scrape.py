import requests
from bs4 import BeautifulSoup
import csv

base_url="https://www.redcross.org/faq.html"

response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

with open("q&a.csv", mode="w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)
    writer.writerow(["Title"])


    table = soup.find_all('div', class_="par-100 col-12 section-par one-col-100 par-1")
 
    for row in table:
    
        text = row.find_all('span', class_="expandable-subtitle")
        for question_text in row:
            if question_text:
                question = question_text.get_text(strip=True)

                writer.writerow([question])
    