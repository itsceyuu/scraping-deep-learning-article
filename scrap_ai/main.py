# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
# import requests
# import time
# import os

# print("🚀 SCRIPT DIMULAI")

# # ======================
# # SETUP
# # ======================
# BASE_URL = "https://www.semanticscholar.org"
# KEYWORDS = [
#     "attention is all you need",
#     "deep learning",
#     "artificial intelligence",
#     "data science"
# ]

# MAX_ARTICLES = 20
# YEAR_MIN = 2017

# os.makedirs("data/pdf", exist_ok=True)
# os.makedirs("data/thumbnail", exist_ok=True)

# # ======================
# # DRIVER
# # ======================
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")

# driver = webdriver.Chrome(
#     service=Service(ChromeDriverManager().install()),
#     options=options
# )

# articles_data = []

# # ======================
# # SCRAPING
# # ======================
# driver.get(BASE_URL)
# time.sleep(3)

# search_box = driver.find_element(By.NAME, "q")
# search_box.send_keys(" OR ".join(KEYWORDS))
# search_box.send_keys(Keys.ENTER)
# time.sleep(5)

# papers = driver.find_elements(By.CSS_SELECTOR, "div.cl-paper-row")

# for paper in papers:
#     if len(articles_data) >= MAX_ARTICLES:
#         break

#     try:
#         paper.find_element(By.TAG_NAME, "a").click()
#         time.sleep(4)

#         title = driver.find_element(By.TAG_NAME, "h1").text

#         year = driver.find_element(
#             By.XPATH, "//span[contains(text(),'Published')]"
#         ).text.split()[-1]

#         if int(year) < YEAR_MIN:
#             driver.back()
#             time.sleep(3)
#             continue

#         authors = driver.find_element(
#             By.CSS_SELECTOR, "span[data-test-id='authors-list']"
#         ).text

#         abstract = driver.find_element(
#             By.CSS_SELECTOR, "span[data-test-id='text-truncator-text']"
#         ).text

#         try:
#             publisher = driver.find_element(
#                 By.XPATH, "//span[contains(text(),'Venue')]"
#             ).text.replace("Venue:", "").strip()
#         except:
#             publisher = "Unknown"

#         try:
#             paper_type = "Conference" if "Proceedings" in publisher else "Journal"
#         except:
#             paper_type = "Journal"

#         keywords = ", ".join(KEYWORDS[:3])

#         # ======================
#         # PDF
#         # ======================
#         pdf_path = ""
#         try:
#             pdf_btn = driver.find_element(By.XPATH, "//a[contains(@href,'.pdf')]")
#             pdf_url = pdf_btn.get_attribute("href")

#             pdf_name = title.replace(" ", "_")[:40] + ".pdf"
#             pdf_path = f"data/pdf/{pdf_name}"

#             r = requests.get(pdf_url, timeout=10)
#             with open(pdf_path, "wb") as f:
#                 f.write(r.content)

#         except:
#             driver.back()
#             time.sleep(3)
#             continue

#         # ======================
#         # THUMBNAIL
#         # ======================
#         thumb_name = title.replace(" ", "_")[:40] + ".png"
#         thumb_path = f"data/thumbnail/{thumb_name}"
#         driver.save_screenshot(thumb_path)

#         # ======================
#         # SAVE
#         # ======================
#         articles_data.append({
#             "judul": title,
#             "tahun": year,
#             "penulis": authors,
#             "publisher": publisher,
#             "tipe": paper_type,
#             "kata_kunci": keywords,
#             "abstrak": abstract,
#             "pdf_path": pdf_path,
#             "thumbnail_path": thumb_path
#         })

#         driver.back()
#         time.sleep(3)

#     except Exception as e:
#         driver.back()
#         time.sleep(3)
#         continue

# # ======================
# # EXPORT CSV
# # ======================
# df = pd.DataFrame(articles_data)
# df.to_csv("articles.csv", index=False, encoding="utf-8")

# driver.quit()

# print("✅ Scraping selesai. CSV berhasil dibuat.")


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
