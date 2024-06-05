from django.contrib import admin
from django.urls import path, include

from mainapp.views import NotFoundView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('mainapp.urls')),
    path('auth/', include('authapp.urls')),
    path('product/', include('productapp.urls')),
    path('not_found/', NotFoundView.as_view(), name='not_found')
]
