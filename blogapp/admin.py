from django.contrib import admin

# Register your models here.
from .models import NewsWebsite
from .models import Article
#from .models import ArticleItem

admin.site.register(NewsWebsite)
admin.site.register(Article)
#admin.site.register(ArticleItem)
