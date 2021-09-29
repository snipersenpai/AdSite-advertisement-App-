from django.contrib import admin
from django.urls import include, path
from .views import *
app_name ='registration'

urlpatterns = [
    path('signup/',UserCreate.as_view(),name='signup'),
]
