from django.contrib.auth import get_user_model 
from django.db import models 
from django.urls import reverse 
from django.utils import timezone 


class Ticker(models.Model):
    name = models.CharField(max_length=15)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Tickers"


class Article(models.Model):
    author = models.CharField(max_length=200) # Not implemented yet, I use the source as the author
    title = models.CharField(max_length=200)
    url = models.URLField()
    source = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    description = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    content = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-published_at']
        verbose_name_plural = "Articles"

