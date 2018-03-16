from django.db import models
from django.utils.translation import ugettext_lazy as _

from coins.constants import BIP44_CHOICES_SYMBOL


class Balance(models.Model):
    """Store balance for a specific coin."""

    coin = models.CharField(
        verbose_name=_('Coin'),
        max_length=32,
        choices=BIP44_CHOICES_SYMBOL)
    balance = models.DecimalField(
        verbose_name=_('Balance'),
        decimal_places=18,
        max_digits=18 + 9)

    class Meta:
        verbose_name = _('Balance')
        verbose_name_plural = _('Balances')
