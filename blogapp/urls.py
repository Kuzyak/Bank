from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^news/$', views.post_list_all, name='post_list_all'),
    url(r'^rate/$', views.rate_ex_bank, name='rate_ex_bank'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
]
