from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='users-ui-login'),
    path('register/', views.register, name='users-ui-register'),
]