from django.conf.urls import url
from . import views
urlpatterns = [
    #url(r'^api/data/$', views.get_data, name='api-data'),
    #url(r'^history/$', views.rate_ex_history, name='rate_ex_history'),
    url(r'^$', views.post_list, name='post_list'),
    url(r'^history/$', views.rate_ex_history.as_view(), name='rate_ex_history'),
    url(r'^api/chart/data/$', views.ChartData.as_view()),
    url(r'^news/$', views.post_list_all, name='post_list_all'),
    url(r'^bank_cards/$', views.bank_cards, name='bank_cards'),
    url(r'^map/$', views.map, name='map'),
    url(r'^rate_bank/$', views.rate_ex_bank, name='rate_ex_bank'),
    url(r'^loan/$', views.loan, name='loan'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^en/$', views.post_list_en, name='post_list_en'),
    url(r'^en/history/$', views.rate_ex_history_en.as_view(), name='rate_ex_history_en'),
    url(r'^en/news/$', views.post_list_all_en, name='post_list_all_en'),
    url(r'^en/bank_cards/$', views.bank_cards_en, name='bank_cards_en'),
    url(r'^en/map/$', views.map_en, name='map_en'),
    url(r'^en/rate_bank/$', views.rate_ex_bank_en, name='rate_ex_bank_en'),
    url(r'^en/loan/$', views.loan_en, name='loan_en'),
    url(r'^en/post/(?P<pk>[0-9]+)/$', views.post_detail_en, name='post_detail_en'),
]
