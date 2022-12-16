from django.urls import path
from . import views

app_name = 'collection'

urlpatterns = [
    path('collection/<int:id>',views.collectionHome,name='home'),
    path('subcategory/<int:id>',views.subCategory,name='subcategory'),
    path('products/<int:id>',views.products,name='products'),
    path('product-details/<int:id>',views.productDetails,name='productdetails'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('order-success/',views.orderSuccess,name='ordersuccess'),
    path('contact/',views.contact,name='contact'),
]