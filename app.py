from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def scrape_news():
    url = "https://agriculturepost.com"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    posts = soup.select("div.hms-post")

    for post in posts:
        title_tag = post.select_one("h3.hms-title a")
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href", "#")
            articles.append({"title": title, "link": link})

    return articles

@app.route("/news", methods=["GET"])
def get_news():
    articles = scrape_news()
    return jsonify(articles)

if __name__ == "__main__":
    app.run(debug=True)