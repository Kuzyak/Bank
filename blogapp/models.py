from django.db import models
import scrapy
from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy_djangoitem import DjangoItem
#from scrapy.contrib_exp.djangoitem import DjangoItem
from django.utils import timezone

class NewsWebsite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(Scraper)
    scraper_runtime = models.ForeignKey(SchedulerRuntime)

    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    EUR = models.CharField(max_length=20)
    USD = models.CharField(max_length=20)
    CHF = models.CharField(max_length=20)
    UAH = models.CharField(max_length=20)
    RUB = models.CharField(max_length=20)
    RON = models.CharField(max_length=20)
    GBP = models.CharField(max_length=20)
    news_website = models.ForeignKey(NewsWebsite)
    description = models.TextField(blank=True)
    url = models.URLField()
    checker_runtime = models.ForeignKey(SchedulerRuntime)

    def __unicode__(self):
        return self.title


class ArticleItem(DjangoItem):
    django_model = Article

'''
# Create your models here.
class KursValue(models.Model):
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
'''
'''
class KursValue(models.Model):
    title = models.CharField(max_length=255)
    val = models.CharField(max_length=255)

    #def __str__(self):
    #    return self.title

class Post(models.Model):
    #author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(
            blank=True, null=True)
    #images = models.ImageField(upload_to='new', blank=True)
    """
    smale_images = ImageSpecField(
        source='images',
        processors=[ResizeToFill(450, 300)],
        format='PNG',
        options={'quality':90})
    """

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.title
# Create your models here.
'''
