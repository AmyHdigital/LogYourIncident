
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('incidents.urls')),
    path('incidents/', include('incidents.urls')),
     path('search/', include('incidents.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]

