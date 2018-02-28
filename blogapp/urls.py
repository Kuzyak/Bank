from django.conf.urls import url
from . import views
urlpatterns = [
    #url(r'^api/data/$', views.get_data, name='api-data'),
    #url(r'^history/$', views.rate_ex_history, name='rate_ex_history'),
    #url(r'^$', views.post_list, name='post_list'),
    #url(r'^history/$', views.rate_ex_history.as_view(), name='rate_ex_history'),
    #url(r'^news/$', views.post_list_all, name='post_list_all'),
    #url(r'^bank_cards/$', views.bank_cards, name='bank_cards'),
    #url(r'^map/$', views.map, name='map'),
    #url(r'^rate_bank/$', views.rate_ex_bank, name='rate_ex_bank'),
    #url(r'^loan/$', views.loan, name='loan'),
    #url(r'^contact/$', views.contact_us, name='contact_us'),
    #url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),

    url(r'^api/chart/data/$', views.ChartData.as_view()),
    url(r'^post_new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^$', views.post_list_en, name='post_list_en'),
    #url(r'^history/$', views.rate_ex_history_en.as_view(), name='rate_ex_history_en'),
    url(r'^news/$', views.post_list_all_en, name='post_list_all_en'),
    #url(r'^bank_cards/$', views.bank_cards_en, name='bank_cards_en'),
    url(r'^icos/$', views.ico_en, name='ico_en'),
    #url(r'^map/$', views.map_en, name='map_en'),
    #url(r'^rate_bank/$', views.rate_ex_bank_en, name='rate_ex_bank_en'),
    #url(r'^loan/$', views.loan_en, name='loan_en'),
    url(r'^contact/$', views.contact_us_en, name='contact_us_en'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail_en, name='post_detail_en'),
]
