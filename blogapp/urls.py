from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^history/$', views.rate_ex_history.as_view(), name='rate_ex_history'),
    #url(r'^api/data/$', views.get_data, name='api-data'),
    url(r'^api/chart/data/$', views.ChartData.as_view()),
    url(r'^news/$', views.post_list_all, name='post_list_all'),
    url(r'^bank_cards/$', views.bank_cards, name='bank_cards'),
    url(r'^map/$', views.map, name='map'),
    url(r'^rate_bank/$', views.rate_ex_bank, name='rate_ex_bank'),
    url(r'^loan/$', views.loan, name='loan'),
    #url(r'^history/$', views.rate_ex_history, name='rate_ex_history'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
]
