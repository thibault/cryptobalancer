from django import template

register = template.Library()


@register.simple_tag
def position_fiat(market, position):
    price = market.get_price(position)
    return '{:.2f}'.format(price)


@register.simple_tag
def positions_fiat(market, positions):
    price = market.get_total_price(positions)
    return '{:.2f}'.format(price)
