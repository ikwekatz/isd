from django.urls import path
from .views import get_sub_services

urlpatterns = [
    path('get_sub_services/', get_sub_services, name='get_sub_services'),
]
