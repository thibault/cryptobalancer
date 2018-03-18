from django import template

register = template.Library()


@register.simple_tag
def position_fiat(market, position):
    price = market.get_price(position)
    return '{:.2f}'.format(price)
