from django.urls import path
from . import views

app_name = 'official'

urlpatterns = [
    path('login-page', views.loginpage, name='loginpage'),
    path('logout',views.logout_shop, name='logout'),

    path('', views.officialHome, name='officialhome'),
    path('newuser-registration', views.newUserRegistration, name='newuserreg'),
    path('customer-list', views.customerList, name='customerlist'),
    path('banners', views.banners, name='banners'),
    path('social-media-links', views.socialMedia, name='socialmedialinks'),
]