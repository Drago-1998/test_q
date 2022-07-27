from django.urls import path

from order.views import HomePageView

urlpatterns = [
    path(r'', HomePageView.as_view(), name='home'),
]
