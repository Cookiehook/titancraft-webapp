from django.urls import path

from app.views.web import static, auth, ref_data, businesses

urlpatterns = [
    path('', static.index, name='index'),

    path('businesses/stock', businesses.list_all_stock, name='get_all_stock'),
    path('businesses/services', businesses.list_all_services, name='get_all_services'),
    path('businesses/<str:business_type>', businesses.list_all_businesses, name='get_all_businesses'),

    path('business/<slug>', businesses.get_single_business, name='get_single_business'),
    path('business/add', static.under_construction, name='add_business'),

    path('user/businesses', static.under_construction, name='get_my_businesses'),

    path('auth/login', auth.request_oauth_token, name='login'),
    path('auth/callback', auth.oauth_callback, name='auth_callback'),
    path('auth/failure', auth.auth_failure, name='auth_failure'),
    path('auth/logout', auth.logout, name='logout'),

    path('refdata/init', ref_data.initialise, name='refdata-init'),
    path('refdata/business', ref_data.create_test_businesses, name='refdata-business'),
]