import requests
from decimal import Decimal as D
from django.core.management.base import BaseCommand
from django.db import transaction

from markets.models import Asset


API_ENDPOINT = 'https://api.coinmarketcap.com/v1/ticker/?convert=EUR'


def fetch_raw_data():
    r = requests.get(API_ENDPOINT)
    if r.status_code != 200:
        raise RuntimeError('Unable to access markets API')

    data = r.json()
    return data


class Command(BaseCommand):
    help = 'Update assets from markets api'

    def handle(self, *args, **options):
        data = fetch_raw_data()
        assets = []
        for asset_data in data:
            assets.append(
                Asset(
                    ticker=asset_data['symbol'],
                    price_eur=D(asset_data['price_eur']),
                    price_usd=D(asset_data['price_usd']),
                    price_btc=D(asset_data['price_btc'])))

        with transaction.atomic():
            Asset.objects.all().delete()
            Asset.objects.bulk_create(assets)
