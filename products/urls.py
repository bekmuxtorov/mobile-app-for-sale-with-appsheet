from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('<int:pk>/', views.product_detail, name='product_detail'),

    path('units/', views.unit_list, name='unit_list'),
    path('units/add/', views.add_unit, name='add_unit'),
    path('units/<int:pk>/', views.unit_detail, name='unit_detail'),
    path('<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('units/<int:pk>/delete/', views.delete_unit, name='delete_unit'),
]
