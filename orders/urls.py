from django.urls import path
from . import views

urlpatterns = [
    path('', views.output_list, name='output_list'),
    path('add/', views.add_output, name='add_output'),
    path('<int:pk>/', views.output_detail, name='output_detail'),
]
