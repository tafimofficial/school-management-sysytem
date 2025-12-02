from django.urls import path
from .views import (
    dashboard, home, custom_login, custom_logout,
    user_list, user_create, user_update, user_delete,
    profile, settings
)

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('settings/', settings, name='settings'),
    
    # User Management
    path('users/', user_list, name='user_list'),
    path('users/create/', user_create, name='user_create'),
    path('users/<int:pk>/edit/', user_update, name='user_update'),
    path('users/<int:pk>/delete/', user_delete, name='user_delete'),
]
