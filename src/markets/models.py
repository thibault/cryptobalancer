from decimal import Decimal as D

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Asset(models.Model):
    '''Market related data about an asset.'''

    ticker = models.CharField(
        verbose_name=_('Ticker'),
        max_length=32,
        db_index=True)
    price_eur = models.DecimalField(
        verbose_name=_('Price (eur)'),
        decimal_places=8,
        max_digits=16)
    price_usd = models.DecimalField(
        verbose_name=_('Price (usd)'),
        decimal_places=8,
        max_digits=16)
    price_btc = models.DecimalField(
        verbose_name=_('Price (btc)'),
        decimal_places=8,
        max_digits=16)

    class Meta:
        verbose_name = _('Asset')
        verbose_name_plural = _('Assets')


class Market:
    '''Utility method to price positions.'''

    def __init__(self):
        self.assets = dict(
            (asset.ticker, asset) for asset in Asset.objects.all())

    def get_price(self, position):
        asset = self.assets.get(position.ticker, None)
        if asset:
            price = position.position * asset.price_eur
        else:
            price = None

        return price

    def get_total_price(self, positions):
        total_price = D('0')
        for position in positions:
            total_price += self.get_price(position) or D('0')

        return total_price
