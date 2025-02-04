from django.urls import path
from .views import login_view, create_request, request_list, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('create_request/', create_request, name='create_request'),
    path('requests/', request_list, name='request_list'),
    path('logout/', logout_view, name='logout'),
]