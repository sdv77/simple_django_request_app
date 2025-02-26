from django.urls import path
from .views import home_view, login_view, create_request, request_list, logout_view, load_devices, change_status, closed_requests

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create-request/', create_request, name='create_request'),
    path('requests/', request_list, name='request_list'),
    path('ajax/load-devices/', load_devices, name='ajax_load_devices'),
    path('change_status/<int:request_id>/', change_status, name='change_status'),
    path('closed_requests/', closed_requests, name='closed_requests'),
]