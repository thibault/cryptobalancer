from django.views.generic import TemplateView


class PortfolioView(TemplateView):
    '''Portfolio display / edition.'''

    template_name = 'portfolio/portfolio.html'
