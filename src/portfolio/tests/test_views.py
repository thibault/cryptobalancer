from decimal import Decimal as D
from django.urls import reverse
import pytest

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
