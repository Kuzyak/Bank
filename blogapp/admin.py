from django.contrib import admin

# Register your models here.
from .models import NewsWebsite
from .models import Article
from .models import Post
from .models import BankCard
from .models import AboutUs

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "created_date", "published_date"]
    list_filter = ["created_date", "published_date"]
    search_fields = ["title","text"]
    class Meta:
        model = Post

class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ["__unicode__"]
    #list_filter = ["created_date", "published_date"]
    class Meta:
        model = Article

admin.site.register(AboutUs)
admin.site.register(BankCard)
admin.site.register(NewsWebsite)
admin.site.register(Article, ArticleModelAdmin)
admin.site.register(Post, PostModelAdmin)
