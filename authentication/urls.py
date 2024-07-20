from django.urls import path
from .views import AuthUserView

urlpatterns = [
    path('register/', AuthUserView.as_view(is_register=True), name='register'),
    path('login/', AuthUserView.as_view(is_register=False), name='login'),
]
