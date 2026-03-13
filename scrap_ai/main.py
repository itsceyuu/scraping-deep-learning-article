from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os
import re

print("🚀 SCRIPT DIMULAI")

# ======================
# CONFIG
# ======================
SEARCH_URL = "https://arxiv.org/search/?query=deep+learning&searchtype=all"
MAX_ARTICLES = 20
YEAR_MIN = 2017

os.makedirs("data/thumbnail", exist_ok=True)

# ======================
# DRIVER
# ======================
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome Safari"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 20)
driver.get(SEARCH_URL)

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "arxiv-result")))

papers = driver.find_elements(By.CLASS_NAME, "arxiv-result")

print(f"🔎 Total result ditemukan: {len(papers)}")

data = []

for idx, paper in enumerate(papers):
    if len(data) >= MAX_ARTICLES:
        break

    try:
        title = paper.find_element(By.CSS_SELECTOR, "p.title").text.strip()
        authors = paper.find_element(By.CSS_SELECTOR, "p.authors").text.replace("Authors:", "").strip()
        abstract = paper.find_element(By.CSS_SELECTOR, "span.abstract-full").text.strip()

        date_text = paper.find_element(By.CSS_SELECTOR, "p.is-size-7").text
        year_match = re.search(r"\d{4}", date_text)
        year = int(year_match.group()) if year_match else 0

        if year < YEAR_MIN:
            continue

        pdf_relative = paper.find_element(By.PARTIAL_LINK_TEXT, "pdf").get_attribute("href")

        # ======================
        # THUMBNAIL (screenshot per item)
        # ======================
        thumb_path = f"data/thumbnail/arxiv_{idx+1}.png"
        paper.screenshot(thumb_path)

        data.append({
            "judul": title,
            "tahun": year,
            "penulis": authors,
            "publisher": "arXiv",
            "tipe": "Preprint",
            "kata_kunci": "AI, Deep Learning, Data Science",
            "abstrak": abstract,
            "pdf_url": pdf_relative,
            "thumbnail_path": thumb_path
        })

        print(f"✅ Diambil: {title[:50]}...")

    except Exception as e:
        print("❌ Skip 1 artikel:", e)
        continue

# ======================
# CSV
# ======================
df = pd.DataFrame(data)
df.to_csv("articles.csv", index=False, encoding="utf-8")

driver.quit()

print(f"🎉 SELESAI — total artikel: {len(df)}")
