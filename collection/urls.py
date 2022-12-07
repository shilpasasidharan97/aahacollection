from django.urls import path
from . import views

app_name = 'collection'

urlpatterns = [
    path('',views.collectionHome,name='home'),
    path('products',views.products,name='products'),
]