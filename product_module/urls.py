from django.urls import path
from . import views
urlpatterns = [
    path('', views.ListProductView.as_view(), name='product_page'),
    path('best-selling', views.BestSellingProductView.as_view(), name='best_selling_page'),
    path('<slug>', views.DetailProductView.as_view(), name='product_detail_page'),

]
