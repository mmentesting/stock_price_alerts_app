import requests
import smtplib
import os

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = os.environ["STOCK_API_KEY"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]
STOCK_NAME = "NFLX"
COMPANY_NAME = "Netflix"

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]

stock_parameters = {
    "function": "GLOBAL_QUOTE",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

news_parameters = {
    "q": COMPANY_NAME,
    "searchIn": "title",
}
news_header = {"X-Api-Key": NEWS_API_KEY}

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
data = stock_response.json()
diff_percent = round(float((data["Global Quote"]["10. change percent"])[:-1]), 1)
if diff_percent > 0:
    up_down = "UP"  # 🡱
else:
    up_down = "DOWN"  # 🡳

if abs(diff_percent) > 2:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters, headers=news_header)
    news_response.raise_for_status()
    news_data = news_response.json()
    articles = news_data["articles"][:3]
    formatted_articles = [f"Headline: {article['title'].encode()}."
                          f"\n'Brief: {article['description'].encode()}" for article in articles]
    # formatted_articles = [f"Headline: {article['title']}.\n'Brief: {article['description']}" for article in articles]
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        for article in formatted_articles:
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL,
                                msg=f"Subject:{STOCK_NAME} {up_down} {diff_percent}%\n\n{article}")
