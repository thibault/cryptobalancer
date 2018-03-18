from django.conf.urls import url

from .views import Portfolio, PositionEdit


urlpatterns = [
    url(r'^$', Portfolio.as_view(), name='portfolio'),
    url(r'^edit/$', PositionEdit.as_view(), name='position_add'),
    url(r'^edit/(?P<ticker>\w+)/$', PositionEdit.as_view(), name='position_edit'),
]
