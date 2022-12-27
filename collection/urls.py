from django.urls import path
from . import views

app_name = 'collection'

urlpatterns = [
    path('collection/<int:id>',views.collectionHome,name='home'),
    path('subcategory/<int:id>',views.subCategory,name='subcategory'),
    path('products/<int:id>',views.products,name='products'),
    path('product-details/<int:id>',views.productDetails,name='productdetails'),

    path("addtocart/<int:pid>/<int:qty>/", views.AddToCart, name="addtocart"),
    
    # path("addquantity/", views.addQuantity, name="addquantity"),
    # path("lessquantity/", views.lessQuantity, name="lessquantity"),
    path('cart/',views.cart,name='cart'),
    path("addquantity/", views.addquantity, name="addquantity"),

    path('checkout/',views.checkout,name='checkout'),
    path('customer-checkout',views.customerCheckout,name='customercheckout'),

    path('new-arrivals/',views.newArrivals,name='newarrivals'),

    # hot deals
    path('hot-deals/',views.hotdeals,name='hotdeals'),

    path('order-success/',views.orderSuccess,name='ordersuccess'),
    path('contact/',views.contact,name='contact'),
    path('contactdata/',views.contactData,name='contactdata'),

]