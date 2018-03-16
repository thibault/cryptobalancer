from django.conf.urls import url

from .views import PortfolioView


urlpatterns = [
    url(r'^$', PortfolioView.as_view(), name='portfolio'),
]
