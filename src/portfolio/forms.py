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
