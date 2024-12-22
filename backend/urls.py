from django.urls import path, include


urlpatterns = [
    path('blogs/', include('backend.blogs_api.urls')), # trialing slash is removed here, so it should be included in the apps > urls.py file if needed
    path('users/', include('backend.users_api.urls')),
]