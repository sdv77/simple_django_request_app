from django.urls import path
from .views import (
    home_view, login_view, create_request, request_list, logout_view,
    load_devices, change_status, closed_requests, download_written_off_act,
    written_off_devices  # Новое представление
)

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create-request/', create_request, name='create_request'),
    path('requests/', request_list, name='request_list'),
    path('ajax/load-devices/', load_devices, name='ajax_load_devices'),
    path('change_status/<int:request_id>/', change_status, name='change_status'),
    path('closed_requests/', closed_requests, name='closed_requests'),
    path('download-act/<int:device_id>/', download_written_off_act, name='download_written_off_act'),
    path('written-off-devices/', written_off_devices, name='written_off_devices'),  # Новый маршрут
]