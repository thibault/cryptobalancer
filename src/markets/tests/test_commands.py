import pytest
from decimal import Decimal as D
from django.core.management import call_command

from markets.models import Asset
from markets.tests.fixtures import API_DATA
from markets.tests.factories import AssetFactory
from markets.management.commands import fetch_market_data


pytestmark = pytest.mark.django_db


def api_mock():
    return API_DATA


def test_fetch_maket_data(monkeypatch):
    monkeypatch.setattr(fetch_market_data, 'fetch_raw_data', api_mock)

    qs = Asset.objects.all()
    assert qs.count() == 0

    call_command('fetch_market_data')
    assert qs.count() == 4


def test_update_existing_data(monkeypatch):
    AssetFactory(ticker='BTC', price_eur=D('42'))
    qs = Asset.objects.all()
    assert qs.count() == 1

    monkeypatch.setattr(fetch_market_data, 'fetch_raw_data', api_mock)

    call_command('fetch_market_data')
    assert qs.count() == 4

    btc = qs.get(ticker='BTC')
    assert btc.price_eur == D("6207.82752405")
