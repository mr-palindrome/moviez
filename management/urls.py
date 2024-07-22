from django.urls import path
from .views import RequestCounterView, ResetRequestCounterView


urlpatterns = [
    path('', RequestCounterView.as_view(), name='request-count'),
    path('reset/', ResetRequestCounterView.as_view(), name='request-count-reset'),
]