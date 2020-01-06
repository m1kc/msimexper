from .views import index, main_handler

from django.urls import path, include


urlpatterns = [
    path('v<int:layer>/<str:ptype>', main_handler),
    path('', index),
]
