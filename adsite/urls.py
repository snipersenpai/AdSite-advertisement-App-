"""adsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.views.generic import TemplateView
from ads.views import MainView

urlpatterns = [
    path('',MainView.as_view(),name='all'),
    path('admin/', admin.site.urls),
    path('ads/', include('ads.urls',namespace='ads')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registration/', include('registration.urls',namespace='registration')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/',include('orders.urls', namespace='orders'))
]

# Serve the favicon - Keep for later
# urlpatterns += [
#     path('favicon.ico', serve, {
#             'path': 'favicon.ico',
#             'document_root': os.path.join(BASE_DIR, 'home/static'),
#         }
#     ),
# ]
