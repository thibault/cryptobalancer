from django.conf.urls import url

from .views import CoinList, CoinAdd


urlpatterns = [
    url(r'^$', CoinList.as_view(), name='coin_list'),
    url(r'^add/$', CoinAdd.as_view(), name='coin_add'),
]
