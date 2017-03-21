from django.db import models
import scrapy
from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy_djangoitem import DjangoItem
#from scrapy.contrib_exp.djangoitem import DjangoItem
from django.utils import timezone

class Post(models.Model):
    #
    #author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=300)
    text = models.TextField()
    published_date = models.DateTimeField(
            blank=True, null=True)
    created_date = models.DateTimeField(
            default=timezone.now)
    images = models.ImageField(upload_to='new', blank=True)
    #smale_images = ImageSpecField(
    #    source='images',
    #    processors=[ResizeToFill(330, 240)],
    #    format='PNG',
    #    options={'quality':90})

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.title

class NewsWebsite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(Scraper)
    scraper_runtime = models.ForeignKey(SchedulerRuntime)

    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    EUR = models.TextField()
    USD = models.TextField()
    CHF = models.TextField()
    CNY = models.TextField()
    RUB = models.TextField()
    GBP = models.TextField()
    RON = models.TextField()
    #
    #created_date = models.DateTimeField(default=timezone.now)
    news_website = models.ForeignKey(NewsWebsite)
    description = models.TextField(blank=True)
    url = models.URLField()
    checker_runtime = models.ForeignKey(SchedulerRuntime)

    def __unicode__(self):
        return self.title


class ArticleItem(DjangoItem):
    django_model = Article
