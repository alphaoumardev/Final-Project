from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup
import time
import csv

# Setup headless Chrome
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# Base URL
base_url = "https://stanford.service-now.com/it_services?id=kb_category&kb_category=012d10f94fbeeac074c9a35e0210c790&kb_id=a508e0f313325e00fe393cc12244b0dc"

driver.get(base_url)
time.sleep(20)  # Let JS load

soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract category links
categories = soup.select('div.list-group a')
data = []

for link in categories:
    category_name = link.text.strip()
    href = link.get('href')
    full_url = "https://stanford.service-now.com/it_services" + href

    driver.get(full_url)
    time.sleep(2)

    while True:
        # Parse page
        category_soup = BeautifulSoup(driver.page_source, 'html.parser')
        faqs = category_soup.select('ul > li')

        for faq in faqs:
            question_tag = faq.select_one('h4 > a')
            answer_tag = faq.select_one('p > span')

            if question_tag and answer_tag:
                question = question_tag.text.strip()
                answer = answer_tag.text.strip()
                data.append({
                    "category": category_name,
                    "question": question,
                    "answer": answer
                })

        # Try to click the "Next" button if it exists
        try:
            next_button = driver.find_element("css selector",
                                              "div.panel-footer div.btn-toolbar div:nth-child(3) > a")

            # Check if the button is disabled (no more pages)
            if 'disabled' in next_button.get_attribute("class"):
                break

            next_button.click()
            time.sleep(2)
        except (NoSuchElementException, ElementClickInterceptedException):
            break  # No more pagination

# Save to CSV
with open('stanford_faq_paginated.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["category", "question", "answer"])
    writer.writeheader()
    writer.writerows(data)

driver.quit()
print("✅ Scraping complete. Data saved to stanford_faq_paginated.csv.")
