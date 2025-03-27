from django.urls import path
from .views import (
    login_view, create_request, request_list, logout_view, change_status, closed_requests,
    load_devices, download_written_off_act, home_view, written_off_devices
)

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('create-request/', create_request, name='create_request'),
    path('requests/', request_list, name='request_list'),
    path('logout/', logout_view, name='logout'),
    path('change_status/<int:request_id>/', change_status, name='change_status'),
    path('closed_requests/', closed_requests, name='closed_requests'),
    path('ajax/load-devices/', load_devices, name='ajax_load_devices'),
    path('download-act/<int:device_id>/', download_written_off_act, name='download_written_off_act'),
    path('written-off-devices/', written_off_devices, name='written_off_devices'),
   
]
