from django.urls import path
from . import views
urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('category', views.category, name='category_page'),
    path('api/search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('api/save-search/', views.save_search_history, name='save_search_history'),
]