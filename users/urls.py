from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customers/add/', views.add_customer, name='add_customer'),
]
