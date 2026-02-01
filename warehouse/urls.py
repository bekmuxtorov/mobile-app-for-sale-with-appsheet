from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_list, name='input_list'),
    path('add/', views.add_input, name='add_input'),
    path('<int:pk>/', views.input_detail, name='input_detail'),
    path('<int:pk>/delete/', views.delete_input, name='delete_input'),
]
