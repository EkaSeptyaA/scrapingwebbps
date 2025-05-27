from flask import Flask, render_template, request
from berita import get_news_links, scrape_news

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    news_data = []
    keyword = ""
    
    if request.method == 'POST':
        topic = request.form['topic']
        sentiment_type = request.form['sentiment_type']
        month = request.form['month']
        year = request.form['year']

        keyword = topic
        links = get_news_links(topic, month, year)
        for link in links:
            news = scrape_news(link, topic, sentiment_type)
            if news:
                news_data.append(news)

    return render_template('index.html', keyword=keyword, news_data=news_data)

if __name__ == '__main__':
    app.run(debug=True)
