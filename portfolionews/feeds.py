from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Article


class RssArticlesFeeds(Feed):
    title = "Portfolio News"
    link = "/stocknews/"
    description = "News about my stock watchlist"

    def items(self):
        return Article.objects.order_by("-published_at")[:100] # Was originally updated_at

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
            return item.published_at

    def item_link(self, item):
            return item.url

    def item_author_name(self, item):
        return item.source + " - " + item.ticker
