from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

# Setup headless Chrome
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# Load UBC FAQ page
url = "https://universitycounsel.ubc.ca/homepage/faqs/"
driver.get(url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
data = []

# Select all accordion headers (questions)
accordion_links = soup.select("a.accordion-toggle.accordion-style1.focus")

for link in accordion_links:
    question = link.get_text(strip=True)
    href = link.get("href")

    if href and href.startswith("#"):
        answer_id = href[1:]  # Remove leading #
        answer_container = soup.find(id=answer_id)

        if answer_container:
            # Grab all <p> tags as the answer content
            paragraphs = answer_container.select("div > p")
            answer = " ".join(p.get_text(strip=True) for p in paragraphs)
            data.append({
                "category": "General FAQ",
                "question": question,
                "answer": answer
            })

driver.quit()

# Save to CSV
with open("ubc_faq.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["category", "question", "answer"])
    writer.writeheader()
    writer.writerows(data)

print(f"✅ Done! {len(data)} Q&A pairs saved to `ubc_faq.csv`.")
