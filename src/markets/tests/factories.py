from decimal import Decimal as D

import factory


class AssetFactory(factory.django.DjangoModelFactory):
    ticker = factory.Sequence(lambda n: '{0:3n}')
    price_eur = D('100')
    price_usd = D('80')
    price_btc = D('0.001')

    class Meta:
        model = 'markets.Asset'
