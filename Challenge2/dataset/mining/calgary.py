from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

# Setup headless browser
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# Target URL
url = "https://ucalgary.service-now.com/it?id=kb_article&sys_id=34d4767b1b5c5e5022ba4158dc4bcb84"
driver.get(url)
time.sleep(5)  # Allow JS to load

# Parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract category
category_tag = soup.select_one(
    "div.kb_article.ng-binding.ng-scope h2 span"
)
category = category_tag.get_text(strip=True) if category_tag else "Unknown Category"

# Collect Q&A pairs
container = soup.select_one("div.kb_article.ng-binding.ng-scope")
qa_data = []

if container:
    elements = container.find_all(["h3", "p"])
    for i in range(len(elements)):
        if elements[i].name == "h3":
            question_tag = elements[i].find("span")
            answer = ""
            # Try to get the next sibling <p> as the answer
            if i + 1 < len(elements) and elements[i + 1].name == "p":
                answer_tag = elements[i + 1].find("span")
                if answer_tag:
                    answer = answer_tag.get_text(strip=True)
            if question_tag:
                question = question_tag.get_text(strip=True)
                qa_data.append({
                    "category": category,
                    "question": question,
                    "answer": answer
                })

# Output to CSV
with open("ucalgary_faq_full.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["category", "question", "answer"])
    writer.writeheader()
    writer.writerows(qa_data)

driver.quit()
print(f"✅ Scraped {len(qa_data)} Q&As and saved to `ucalgary_faq_full.csv`.")
