from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs, name='blogs-blogs'),
    path('<int:id>', views.blog, name='blogs-blog'),
]