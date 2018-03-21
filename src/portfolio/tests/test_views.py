from decimal import Decimal as D
from django.urls import reverse
import pytest

from markets.tests.factories import AssetFactory
from portfolio.tests.factories import PositionFactory
from portfolio.models import Position


pytestmark = pytest.mark.django_db


def test_position_edit_with_no_ticker(client):
    url = reverse('position_add')
    res = client.get(url)
    assert res.status_code == 200


def test_add_new_position(client):
    qs = Position.objects.all()
    assert qs.count() == 0

    data = {
        'ticker': 'BTC',
        'position': '42',  # I wish
        'target': '50',
    }
    url = reverse('position_add')
    res = client.post(url, data)
    assert res.status_code == 302
    assert qs.count() == 1

    position = qs[0]
    assert position.ticker == 'BTC'
    assert position.position == D('42')
    assert position.target == D('50')


def test_override_existing_position(client):
    PositionFactory(ticker='BTC', position=D('10'), target=D('10'))
    qs = Position.objects.all()
    assert qs.count() == 1

    data = {
        'ticker': 'BTC',
        'position': '42',  # I wish
        'target': '50',
    }
    url = reverse('position_add')
    res = client.post(url, data)
    assert res.status_code == 302
    assert qs.count() == 1

    position = qs[0]
    assert position.ticker == 'BTC'
    assert position.position == D('42')
    assert position.target == D('50')


def test_edit_existing_position(client):
    PositionFactory(ticker='TOTO', position=D('42.42'), target=D('43.43'))
    qs = Position.objects.all()
    assert qs.count() == 1

    url = reverse('position_edit', args=['TOTO'])
    res = client.get(url)
    content = res.content.decode('utf-8')
    assert 'TOTO' in content
    assert '42.42' in content
    assert '43.43' in content

    data = {
        'ticker': 'TOTO',
        'position': '42',
        'target': '50',
    }
    res = client.post(url, data)
    assert res.status_code == 302
    assert qs.count() == 1

    position = qs[0]
    assert position.ticker == 'TOTO'
    assert position.position == D('42')
    assert position.target == D('50')


def test_delete_existing_position(client):
    PositionFactory(ticker='BTC', position=D('10'), target=D('10'))
    qs = Position.objects.all()
    assert qs.count() == 1

    data = {
        'ticker': 'BTC',
        'position': '0',
        'target': '0',
    }
    url = reverse('position_add')
    res = client.post(url, data)
    assert res.status_code == 302
    assert qs.count() == 0


def test_portfolio_display_fiat_total(client):
    PositionFactory(ticker='BTC', position=D('1'))
    AssetFactory(ticker='BTC', price_eur=D('10'))

    PositionFactory(ticker='ETH', position=D('1'))
    AssetFactory(ticker='ETH', price_eur=D('7'))

    PositionFactory(ticker='DOGE', position=D('1'))
    AssetFactory(ticker='DOGE', price_eur=D('42'))

    url = reverse('portfolio')
    res = client.get(url)
    assert u'<th class="fiat_total">59.00€</th>' in res.content.decode('utf-8')


def test_portfolio_display_percent_target(client):
    PositionFactory(ticker='BTC', position=D('1'), target=D('100'))
    PositionFactory(ticker='ETH', position=D('1'), target=D('60'))
    PositionFactory(ticker='DOGE', position=D('1'), target=D('20'))
    PositionFactory(ticker='NANO', position=D('1'), target=D('20'))

    url = reverse('portfolio')
    res = client.get(url)
    content = res.content.decode()
    assert u'<td>100 (50%)</td>' in content
    assert u'<td>60 (30%)</td>' in content
    assert u'<td>20 (10%)</td>' in content
