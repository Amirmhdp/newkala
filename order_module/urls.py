from django.urls import path
from . import views
urlpatterns = [
    path('', views.order, name='order_page'),
    path('add-product-to-order', views.add_product_to_order, name='add_product_to_order'),
    path('change-count-product', views.change_count_product, name='change_count_product'),
    path('request-payment/', views.request_payment, name='request_payment'),
    path('verify-payment/', views.verify_payment, name='verify_payment')
]
