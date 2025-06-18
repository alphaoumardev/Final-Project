from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# Stanford IT Services base URL
base_url = "https://harvard.service-now.com/ithelp?id=kb_category&kb_category=6abcedfc370176009aa163d2b3990e3a"

driver.get(base_url)
time.sleep(10)  # Wait for page to load JavaScript

soup = BeautifulSoup(driver.page_source, 'html.parser')

categories = soup.select('div.list-group a')
# print(categories.)
# none
data = []

for link in categories:
    category_name = link.text.strip()
    # print(category_name)
    href = link.get('href')
    full_url = "https://harvard.service-now.com/ithelp" + href

    # print(f"Scraping category: {category_name}")
    driver.get(full_url)
    time.sleep(2)

    category_soup = BeautifulSoup(driver.page_source, 'html.parser')

    faqs = category_soup.select('div.panel-body > div')
    for faq in faqs:
        question_tag = faq.select_one('h4 > a')
        answer_tag = faq.select_one('div.ng-binding')

        # print(question_tag.text.strip())
        if question_tag and answer_tag:
            question = question_tag.text.strip()
            answer = answer_tag.text.strip()
            data.append({
                "category": category_name,
                "question": question,
                "answer": answer
            })

# Save to CSV
with open('havard_faq1.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["category", "question", "answer"])
    writer.writeheader()
    writer.writerows(data)

driver.quit()
print("Scraping complete. Data saved to havard_faq.csv.")

