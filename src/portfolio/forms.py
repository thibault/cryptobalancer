from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Position


class PositionForm(forms.ModelForm):

    class Meta:
        exclude = []
        model = Position
        help_texts = {
            'target': _('How much does this asset should weight in your \
                        portfolio? If the sum of all "target" values is not \
                        equal to 100, we will automatically compute the \
                        corresponding percentages.')
        }


class RebalanceForm(forms.Form):
    STRATEGIES = [
        ('buy_and_sell', 'Sell overweighted assets and buy underweightes assets.'),
        ('buy_only', 'Only rebalance by buying more underweighted assets.'),
    ]

    invest_amount = forms.DecimalField(
        label=_('Investing amount'),
        help_text=_('Do you wish to invest some more fiat while rebalancing?'))
    strategy = forms.ChoiceField(
        label=_('Rebalance strategy'),
        help_text=_('Selling assets will allow for faster rebalancing, but \
                    could provoke additional costs.'),
        choices=STRATEGIES)
