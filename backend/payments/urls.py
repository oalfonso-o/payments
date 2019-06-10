from django.contrib import admin
from django.urls import path

from .api import api_urls

urlpatterns = api_urls + [
    path('admin/', admin.site.urls),
]
