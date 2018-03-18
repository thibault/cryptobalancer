from decimal import Decimal
from random import randint

import factory


class PositionFactory(factory.django.DjangoModelFactory):
    ticker = factory.Sequence(lambda n: '{0:3n}')
    position = factory.lazy_attribute(lambda o: Decimal(randint(5, 100)))
    target = Decimal('1')

    class Meta:
        model = 'portfolio.Position'
