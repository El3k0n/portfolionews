# -*- coding: utf-8 -*-
import yfinance as yf 
from newspaper import Article
from newspaper.article import ArticleException 

#import requests
#import csv
#from io import StringIO


def get_news_yfinance(ticker):
    '''
    Gets news for a single ticker from yfinance
    Returns list of dictionaries with the keys:
        - Title
        - Source
        - Date
        - Url
        - Description
        - Category
        - Ticker
        - Content
    '''
    tick = yf.Ticker(ticker)
    news = tick.news

    articles_list = []

    for item in news:
        article = {}

        article["Title"] = item["content"]["title"]
        article["Source"] = item["content"]["provider"]["displayName"]
        article["Date"] = item["content"]["pubDate"]
        article["Url"] = item["content"]["canonicalUrl"]["url"]
        article["Description"] = item["content"]["summary"]
        article["Category"] = ""
        article["Ticker"] = ticker

        try:
            parsed_article = Article(article["Url"])
            parsed_article.download()
            parsed_article.parse()

            article["Content"] = parsed_article.text

        except ArticleException:
            article["Content"] = ""
        
        articles_list.append(article)

    return articles_list

'''
def get_news_finviz(api_key, portfolio_id):
    '''
    Deprecated, use get_news_yfinance instead
    Gets Finviz api key and portfolio id
    Returns list of dictionaries with the keys:
        - Title
        - Source
        - Date
        - Url
        - Category
        - Ticker
        - Content
    '''
    url = "".join(["https://elite.finviz.com/news_export.ashx?pid=", portfolio_id,"&auth=", api_key])
    #print(url)
    response_csv = requests.get(url)
    response_csv.raise_for_status()

    # Convert the response text into a file-like object
    csv_file = StringIO(response_csv.text)

    # Parse the CSV into a dictionary
    reader = csv.DictReader(csv_file)

    # Now iterate through the csv and get the contents in a list
    articles_list = []
    for item in reader:
        articles_list.append(item)

    # For each article get the contents and assign them to the dictionary
    # TODO: Move this part outside this funcion to avoid wasting time downloading the text when the article is already present in the DB
    for item in articles_list:
        try:
            article_url = item['Url']
            article = Article(article_url)
            article.download()
            article.parse()

            item["Content"] = article.text
        except ArticleException:
            item["Content"] = ""

    return articles_list

'''