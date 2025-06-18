# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import time
# import csv
#
# options = Options()
# options.headless = True
# driver = webdriver.Chrome(options=options)
#
# BASE_URL = "https://www.concordia.ca"
# SERVICE_LIST_URL = f"{BASE_URL}/it/services.html"
#
# driver.get(SERVICE_LIST_URL)
# time.sleep(2)
#
# soup = BeautifulSoup(driver.page_source, "html.parser")
# faq_links = [BASE_URL + a["href"] for a in soup.select("a.service-link.alphabar-title")]
#
# faq_data = []
#
# for link in faq_links:
#     category_name = link.get_text(strip=True)
#     driver.get(link)
#     time.sleep(2)
#
#     # Click FAQ toggles
#     try:
#         buttons = driver.find_elements(By.CSS_SELECTOR, "h3 button")
#         for btn in buttons:
#             try:
#                 btn.click()
#                 time.sleep(0.2)
#             except:
#                 pass
#     except:
#         continue
#
#     page_soup = BeautifulSoup(driver.page_source, "html.parser")
#     faqs = page_soup.select("div.faq_parsys.parsys > div")
#
#     for item in faqs:
#         try:
#             question = item.select_one("h3 button span")
#             answer = item.select_one("div.accordion-body div p")
#             if question and answer:
#                 faq_data.append({
#                     "service_url": link,
#                     "question": question.get_text(strip=True),
#                     "answer": answer.get_text(strip=True)
#                 })
#         except:
#             pass
#
# driver.quit()
#
# # Save to CSV
# # with open("concordia_faq_dataset.csv", "w", newline='', encoding='utf-8') as f:
# #     writer = csv.DictWriter(f, fieldnames=["service_url", "question", "answer"])
# #     writer.writeheader()
# #     writer.writerows(faq_data)
# #
# # print("✅ Scraping completed. File saved as `concordia_faq_dataset.csv`.")
#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

BASE_URL = "https://www.concordia.ca"
SERVICE_LIST_URL = f"{BASE_URL}/it/services.html"

driver.get(SERVICE_LIST_URL)
time.sleep(2)

soup = BeautifulSoup(driver.page_source, "html.parser")

faq_data = []

# Loop through all service links
for a in soup.select("a.service-link.alphabar-title"):
    category_name = a.get_text(strip=True)  # ← this is now the title text
    href = a["href"]
    full_url = BASE_URL + href

    driver.get(full_url)
    time.sleep(2)

    # Expand FAQ answers by clicking toggle buttons
    try:
        buttons = driver.find_elements(By.CSS_SELECTOR, "h3 button")
        for btn in buttons:
            try:
                btn.click()
                time.sleep(0.2)
            except:
                pass
    except:
        continue

    page_soup = BeautifulSoup(driver.page_source, "html.parser")
    faqs = page_soup.select("div.faq_parsys.parsys > div")

    for item in faqs:
        try:
            question = item.select_one("h3 button span")
            answer = item.select_one("div.accordion-body div p")
            if question and answer:
                faq_data.append({
                    "service_title": category_name,  # title instead of URL
                    "question": question.get_text(strip=True),
                    "answer": answer.get_text(strip=True)
                })
        except:
            pass

driver.quit()

# Save to CSV
with open("data.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["service_title", "question", "answer"])
    writer.writeheader()
    writer.writerows(faq_data)

print("✅ Scraping completed. File saved as `concordia_faq_dataset.csv`.")
