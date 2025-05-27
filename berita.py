from googlesearch import search
from bs4 import BeautifulSoup
import requests
import time
import re

# Fungsi pencarian berita
def get_news_links(topic, month=None, year=None, num_results=5):
    query = f"{topic} site:kompas.com OR site:detik.com OR site:cnnindonesia.com OR site:tribunnews.com"
    
    if month:
        query += f" {month}"
    if year:
        query += f" {year}"

    news_links = []
    try:
        for url in search(query, num_results=num_results, lang="id"):
            news_links.append(url)
            time.sleep(1)
    except Exception as e:
        print(f"⚠️ Error saat mencari berita: {e}")
    
    return news_links

# Fungsi analisis sentimen sederhana
def detect_sentiment(summary, sentiment_type):
    positive_keywords = ["naik", "meningkat", "stabil", "bertambah", "baik"]
    negative_keywords = ["turun", "merosot", "menurun", "krisis", "buruk"]

    text = summary.lower()
    if sentiment_type == "harga":
        if any(word in text for word in positive_keywords):
            return "Positif"
        elif any(word in text for word in negative_keywords):
            return "Negatif"
    elif sentiment_type == "produksi":
        if any(word in text for word in positive_keywords):
            return "Positif"
        elif any(word in text for word in negative_keywords):
            return "Negatif"
    return "Tidak Teridentifikasi"

# Scraper per berita
def scrape_news(url, topic, sentiment_type):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1").text.strip() if soup.find("h1") else "Judul tidak ditemukan"
        date_tag = soup.find("time")
        date = date_tag.text.strip() if date_tag else "Tanggal tidak ditemukan"

        paragraphs = soup.find_all("p")
        summary = " ".join(p.text.strip() for p in paragraphs[:3])

        sentiment = detect_sentiment(summary, sentiment_type)
        domain_match = re.findall(r'https?://(?:www\.)?([^/]+)', url)
        source = domain_match[0] if domain_match else "Tidak diketahui"

        return {
            "title": title,
            "topic": topic,
            "summary": summary,
            "sentiment_type": sentiment_type.capitalize(),
            "sentiment": sentiment,
            "source": source,
            "date": date,
            "url": url
        }

    except Exception as e:
        print(f"⚠️ Gagal mengambil data dari {url}: {e}")
        return None
