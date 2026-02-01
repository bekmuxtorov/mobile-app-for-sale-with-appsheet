from django.urls import path
from . import views

urlpatterns = [
    path('customer-sales/', views.customer_sales_report,
         name='customer_sales_report'),
    path('product-sales/', views.product_sales_report,
         name='product_sales_report'),
]
