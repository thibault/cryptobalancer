from decimal import Decimal as D

from django import template

register = template.Library()


@register.simple_tag
def position_fiat(market, position):
    price = market.get_price(position)
    return price


@register.simple_tag
def positions_fiat(market, positions):
    price = market.get_total_price(positions)
    return price


@register.simple_tag
def ratio(val, max_val):
    return val / max_val * D('100')


@register.simple_tag
def sub(val1, val2):
    return val1 - val2


@register.filter(name='abs')
def absolute(val):
    return abs(val)
