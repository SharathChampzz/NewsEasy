from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

# /api/users/*
urlpatterns = [
    path('login', views.login, name='users-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', views.logout, name='users-logout'),
    path('', views.users, name='users-users'), # GET and POST users
    path('<int:pk>', views.user_detail, name='users-get_user'), # GET, PUT, DELETE user
]