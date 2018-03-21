from decimal import Decimal as D
from django.views.generic import UpdateView, ListView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

from markets.models import Market
from .models import Position
from .forms import PositionForm, RebalanceForm


REBALANCE_THRESHOLD = D('5')


class Portfolio(FormMixin, ListView):
    '''Portfolio display / edition.'''

    template_name = 'portfolio/portfolio.html'
    context_object_name = 'positions'
    form_class = RebalanceForm
    initial = {
        'invest_amount': D('0'),
    }

    def get_queryset(self):
        qs = Position.objects \
            .order_by('-target', '-position', 'ticker')

        return qs

    def get_context_data(self, **kwargs):
        market = Market()
        total_weight = sum(position.target for position in self.object_list)
        total_fiat = market.get_total_price(self.object_list)

        positions = []
        for position in self.object_list:
            current_fiat = market.get_price(position)
            current_weight = current_fiat / total_fiat * D('100')
            target_weight = position.target / total_weight * D('100')
            target_fiat = target_weight * total_fiat / D('100')
            fiat_delta = target_fiat - current_fiat
            weight_delta = target_weight - current_weight
            positions.append({
                'ticker': position.ticker,
                'position': position.position,
                'current_fiat': current_fiat,
                'current_weight': current_weight,
                'target_fiat': target_fiat,
                'target_weight': target_weight,
                'fiat_delta': fiat_delta,
                'weight_delta': weight_delta,
            })

        kwargs['positions'] = positions
        kwargs['total_weight'] = total_weight
        kwargs['total_fiat'] = market.get_total_price(self.object_list)
        kwargs['threshold'] = REBALANCE_THRESHOLD

        return super().get_context_data(**kwargs)


class PositionEdit(UpdateView):
    '''Add position to portfolio.'''

    template_name = 'portfolio/position_edit.html'
    form_class = PositionForm

    def get_object(self):
        ticker = self.request.POST.get(
            'ticker',
            self.kwargs.get('ticker', None))
        if ticker:
            try:
                position = Position.objects.get(ticker=ticker)
            except Position.DoesNotExist:
                position = Position(ticker=ticker)
        else:
            position = Position(ticker=ticker)
        return position

    def form_valid(self, form):
        if all((
                self.object.id,
                form.cleaned_data['target'] == D('0'),
                form.cleaned_data['position'] == D('0'))):
            self.object.delete()
        else:
            self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('portfolio')
