from django.views.generic import CreateView, ListView
from django.urls import reverse

from .models import Balance
from .forms import BalanceForm


class CoinList(ListView):
    '''Portfolio display / edition.'''

    template_name = 'portfolio/coin_list.html'
    context_object_name = 'coins'

    def get_queryset(self):
        qs = Balance.objects \
            .order_by('-balance', 'coin')
        return qs


class CoinAdd(CreateView):
    '''Add coin to portfolio.'''

    template_name = 'portfolio/coin_add.html'
    form_class = BalanceForm

    def get_success_url(self):
        return reverse('coin_list')
