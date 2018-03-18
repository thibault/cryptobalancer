from decimal import Decimal as D
from django.views.generic import UpdateView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Position
from .forms import PositionForm


class Portfolio(ListView):
    '''Portfolio display / edition.'''

    template_name = 'portfolio/portfolio.html'
    context_object_name = 'positions'

    def get_queryset(self):
        qs = Position.objects \
            .order_by('-position', 'ticker')
        return qs


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
