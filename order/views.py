from django.views.generic import TemplateView

from order.models import Order
from order.tasks import import_data

SPREADSHEET_ID = '1MHO3gRzWEzoG_DMJR7v4140MWaxjW4XZ4A1pX9Uc8ZA'


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        import_data.delay()
        return context
