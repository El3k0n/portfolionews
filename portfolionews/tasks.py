from portfolionews.models import Article, Ticker
from portfolionews.fetch_news import get_news_yfinance
from sqids import Sqids #type: ignore
from random import randint
from dateutil import parser #type: ignore
from datetime import timedelta
from django.utils import timezone #type: ignore


def update_news():
    '''
    This task is called every hour to update the database with news.
    Gets all tickers from the database and fetches news for each ticker using the get_news_yfinance function.
    For each news item obtained, if it's more recent than 1 hour, it saves it to the database.
    '''
    now = timezone.now()
    tickers = Ticker.objects.all()
    s = Sqids(min_length=10)

    for ticker in tickers:
        try:
            news = get_news_yfinance(ticker.symbol)
            
            for item in news:
                dt = parser.parse(item["Date"])
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt)
                
                # Check if news is more recent than 1 hour
                is_recent = now - dt < timedelta(hours=1)
                
                if is_recent:
                    # Check if article already exists to avoid duplicates
                    if not Article.objects.filter(url=item["Url"]).exists():
                        article = Article(
                            author=item["Source"],  # Using source as author as per model comment
                            title=item["Title"],
                            url=item["Url"],
                            source=item["Source"],
                            category=item["Category"],
                            ticker=ticker,
                            description=item["Description"],
                            slug=s.encode([randint(0, 10000), randint(0, 10000)]),
                            content=item["Content"],
                            published_at=dt,
                            is_live=True
                        )
                        article.save()
        except Exception as e:
            # Log error but continue with other tickers
            print(f"Error fetching news for ticker {ticker.symbol}: {e}")
            continue


def populate_first_time():
    '''
    This task is called only once to populate the database with news.
    Gets all tickers from the database and fetches news for each ticker using the get_news_yfinance function.
    For each news item obtained, it saves it to the database.
    '''
    tickers = Ticker.objects.all()
    s = Sqids(min_length=10)

    for ticker in tickers:
        try:
            news = get_news_yfinance(ticker.symbol)
            
            for item in news:
                dt = parser.parse(item["Date"])
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt)
                
                # Check if article already exists to avoid duplicates
                if not Article.objects.filter(url=item["Url"]).exists():
                    article = Article(
                        author=item["Source"],  # Using source as author as per model comment
                        title=item["Title"],
                        url=item["Url"],
                        source=item["Source"],
                        category=item["Category"],
                        ticker=ticker,
                        description=item["Content"][:500] if item["Content"] else "",  # Truncate description
                        slug=s.encode([randint(0, 10000), randint(0, 10000)]),
                        content=item["Content"],
                        published_at=dt,
                        is_live=True
                    )
                    article.save()
        except Exception as e:
            # Log error but continue with other tickers
            print(f"Error fetching news for ticker {ticker.symbol}: {e}")
            continue


'''
Deprecated functions, I'm keeping them here for reference
I'm using yfinance instead of finviz because it's free and has a better API

def update_news():
    now = timezone.now()
    news = get_news_finviz(FINVIZ_API_KEY, FINVIZ_PORTFOLIO_ID)
    s = Sqids(min_length=10)

    for item in news:
        dt = parser.parse(item["Date"])
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)
        is_recent = now - dt < timedelta(hours=1)

        if is_recent:
            article = Article(
                author = "",
                title = item["Title"],
                url = item["Url"],
                description = item["Content"],
                slug = s.encode([randint(0,10000), randint(0,10000)]),
                content = item["Content"],
                published_at = dt,
                is_live = True
            )

            article.save()


def populate_first_time():
    news = get_news(FINVIZ_API_KEY, FINVIZ_PORTFOLIO_ID)
    s = Sqids(min_length=10)

    for item in news:
        dt = parser.parse(item["Date"])
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)

        article = Article(
            author = "",
            title = item["Title"],
            url = item["Url"],
            source = item["Source"],
            category = item["Category"],
            ticker = item["Ticker"],
            description = item["Content"],
            slug = s.encode([randint(0,10000), randint(0,10000)]),
            content = item["Content"],
            published_at = dt,
            is_live = True
        )

        article.save()
'''