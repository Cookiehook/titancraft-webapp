from django.urls import path

from app.views import add, auth, delete, list, location, modify

urlpatterns = [
    path('', auth.index, name='index'),
    path('auth/failure/', auth.auth_failure, name='auth_failure'),
    path('auth/login/', auth.login, name='login'),
    path('auth/callback/', auth.verify_callback, name='verify_callback'),
    path('auth/logout/', auth.logout, name='logout'),
    path('not_authorised/', auth.not_authorised, name='not_authorised'),

    path('stock/', list.list_stock, name='list_stock'),
    path('services/', list.list_services, name='list_services'),
    path('farms/', list.list_farms, name='list_farms'),
    path('locations/<str:region>/', list.list_locations, name='list_locations'),
    path('locations/manage', location.manage_locations, name='manage_locations'),

    path('locations/add', add.add_location, name='add_location'),
    path('locations/maintainers/add', add.add_maintainer, name='add_maintainer'),

    path('location/maintainers/delete', delete.delete_maintainer, name='delete_maintainer'),

    path('location/<str:slug>', location.get_location, name='get_location'),
    path('location/<str:slug>/modify', modify.modify_location, name='modify_location'),
    path('location/<str:slug>/maintainers/modify', modify.modify_maintainers, name='modify_maintainers'),
    path('location/<str:slug>/stock/modify', modify.modify_stock, name='modify_stock'),
    path('location/<str:slug>/services/modify', modify.modify_services, name='modify_services'),
    path('location/<str:slug>/farmables/modify', modify.modify_farmables, name='modify_farmables'),
]
