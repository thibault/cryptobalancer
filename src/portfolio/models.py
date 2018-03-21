from django.db import models
from django.utils.translation import ugettext_lazy as _


class Position(models.Model):
    """Store position for a specific ticker."""

    ticker = models.CharField(
        verbose_name=_('Ticker'),
        max_length=32)
    position = models.DecimalField(
        verbose_name=_('Position'),
        decimal_places=18,
        max_digits=18 + 9)
    target = models.DecimalField(
        verbose_name=_('Target'),
        help_text=_('How much does this asset should weight in your \
                    portfolio?'),
        decimal_places=2,
        max_digits=8)

    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')
        unique_together = ['ticker']
