from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('',views.websiteHome, name='websitehome'),
    path('registration',views.registration, name='registration'),
]