from django.urls import path
from . import views

app_name = 'collection'

urlpatterns = [
    path('',views.collectionHome,name='home'),
    path('subcategory/',views.subCategory,name='subcategory'),
    path('products/',views.products,name='products'),
    path('product-details/',views.productDetails,name='productdetails'),
    path('cart/',views.cart,name='cart'),
]