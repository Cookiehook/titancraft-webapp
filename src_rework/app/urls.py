from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/failure/', views.auth_failure, name='auth_failure'),
    path('auth/login/', views.login, name='login'),
    path('auth/callback/', views.verify_callback, name='verify_callback'),
    path('auth/logout/', views.logout, name='logout'),

    path('stock/', views.list_stock, name='list_stock'),
    path('services/', views.list_services, name='list_services'),
    path('farms/', views.list_farms, name='list_farms'),
    path('locations/<str:dimension>/', views.list_locations, name='list_locations'),
    path('locations/manage', views.manage_locations, name='manage_locations'),
    path('locations/add', views.add_location, name='add_location'),
    path('location/<str:slug>', views.get_location, name='get_location'),
]
