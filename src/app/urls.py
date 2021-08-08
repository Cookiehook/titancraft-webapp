from django.urls import path

from app.views import post_upsert, auth, post_delete, get_list, get_location, get_modify, ref_data

urlpatterns = [
    path('', auth.index, name='index'),
    path('auth/failure/', auth.auth_failure, name='auth_failure'),
    path('auth/login/', auth.login, name='login'),
    path('auth/callback/', auth.verify_callback, name='verify_callback'),
    path('auth/logout/', auth.logout, name='logout'),
    path('not_authorised/', auth.not_authorised, name='not_authorised'),

    path('how-to/', get_list.how_to, name='how_to'),
    path('stock/', get_list.list_stock, name='list_stock'),
    path('services/', get_list.list_services, name='list_services'),
    path('farms/', get_list.list_farms, name='list_farms'),
    path('locations/', get_list.list_locations, name='list_locations'),
    path('locations/manage', get_location.manage_locations, name='manage_locations'),
    path('paths/manage', get_location.manage_paths, name='manage_paths'),

    path('locations/add', post_upsert.upsert_location, name='add_location'),
    path('locations/maintainers/add', post_upsert.upsert_maintainer, name='add_maintainer'),
    path('locations/stock/add', post_upsert.upsert_stock, name='add_stock'),
    path('locations/service/add', post_upsert.upsert_service, name='add_service'),
    path('locations/farm/add', post_upsert.upsert_farm, name='add_farm'),
    path('path/add', post_upsert.upsert_path, name='add_path'),

    path('location/maintainers/delete', post_delete.delete_maintainer, name='delete_maintainer'),
    path('location/stock/delete', post_delete.delete_stock, name='delete_stock'),
    path('location/service/delete', post_delete.delete_service, name='delete_service'),
    path('location/farm/delete', post_delete.delete_farm, name='delete_farm'),
    path('location/location/delete', post_delete.delete_location, name='delete_location'),
    path('path/delete', post_delete.delete_path, name='delete_path'),

    path('location/<int:id>', get_location.get_location, name='get_location'),
    path('location/<int:id>/location/modify', get_modify.modify_location, name='modify_location'),
    path('location/<int:id>/stock/modify', get_modify.modify_stock, name='modify_stock'),
    path('location/<int:id>/services/modify', get_modify.modify_service, name='modify_service'),
    path('location/<int:id>/farm/modify', get_modify.modify_farm, name='modify_farm'),
    path('path/modify', get_modify.modify_path, name='modify_new_path'),
    path('path/<int:id>/modify', get_modify.modify_path, name='modify_path'),

    path('stock/update_availability', post_upsert.update_availability, name='update_availability'),

    path('refdata/init/', ref_data.initialise, name='refdata_initialise'),
]
