from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import re
import time

# Setup headless browser
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# Target URL
url = "https://itsc.ontariotechu.ca/resources/faqs/faqs-ontariotechu.net.php"
driver.get(url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
data = []

# Get all h2 headers (categories)
categories = soup.select("#page-content > div:nth-child(3) > h2")

for cat in categories:
    category_title = cat.get_text(strip=True)

    # Find all accordion labels (questions) and contents (answers) after this category
    next_element = cat.find_next_sibling()
    while next_element and next_element.name != "h2":
        if next_element.has_attr("id") and "accordion" in next_element["id"]:
            match = re.match(r"accordion(\d+)-label", next_element["id"])
            if match:
                num = match.group(1)
                question = next_element.get_text(strip=True)
                answer_elem = soup.select_one(f"#accordion{num}")
                answer = answer_elem.get_text(strip=True) if answer_elem else ""
                data.append({
                    "category": category_title,
                    "question": question,
                    "answer": answer
                })
        next_element = next_element.find_next_sibling()

driver.quit()

# Save to CSV
with open("ontariotech_faq.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["category", "question", "answer"])
    writer.writeheader()
    writer.writerows(data)

print(f"✅ Done! Scraped {len(data)} Q&A pairs into `ontariotech_faq.csv`.")
