from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv

# Setup headless Chrome
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

# Target URL
url = "https://queensu.service-now.com/esm?id=kb_search&spa=1"
driver.get(url)
time.sleep(5)  # Let JavaScript load

# Scroll until all Q&A blocks are loaded
loaded_blocks = set()
max_attempts = 15  # safety cap
attempts = 0

while attempts < max_attempts:
    current_blocks = driver.find_elements(By.CSS_SELECTOR, "div.kb-template.ng-scope")
    current_count = len(current_blocks)

    if current_count > len(loaded_blocks):
        loaded_blocks.update(current_blocks)
        attempts = 0  # reset attempt counter
    else:
        attempts += 1

    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(2)

# Get page HTML
soup = BeautifulSoup(driver.page_source, "html.parser")
data = []

# Locate question and answer containers
faq_blocks = soup.select("div.kb-template.ng-scope")

for block in faq_blocks:
    try:
        question_tag = block.select_one("h3 > a")
        answer_tag = block.select_one("div.kb-description.ng-binding")

        if question_tag and answer_tag:
            question = question_tag.get_text(strip=True)
            answer = answer_tag.get_text(strip=True)
            data.append({
                "category": "General FAQ",
                "question": question,
                "answer": answer
            })
    except Exception as e:
        print("Skipping item due to error:", e)
        continue

driver.quit()

# Save to CSV
with open("queens_faq.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["category", "question", "answer"])
    writer.writeheader()
    writer.writerows(data)

print(f"✅ Done! {len(data)} Q&A pairs saved to `queens_faq.csv`.")
