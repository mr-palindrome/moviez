from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieAPIView, CollectionViewSet

router = DefaultRouter()
router.register(r'collections', CollectionViewSet, basename='collection')

urlpatterns = [
    path('movies/', MovieAPIView.as_view(), name='login'),
    path('', include(router.urls)),
]
