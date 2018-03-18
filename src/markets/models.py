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
