from django.urls import path
from .views import get_orders, create_order


urlpatterns = [
    path('orders/<str:date>/', get_orders, name='get_orders'),
    path('order/', create_order, name='create_order'),
]
