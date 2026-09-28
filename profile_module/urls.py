from django.urls import path
from . import views
urlpatterns = [
    path('', views.UserPanelView.as_view(), name='user_panel_page'),
    path('loaded-cities', views.load_cities, name='cities'),
    path('delete-address', views.delete_address, name='delete_address'),
    path('delete-wishes', views.wishes_delete, name='delete_wishes'),
    path('notifications', views.NotificationsView.as_view(), name='notifications_page'),
]