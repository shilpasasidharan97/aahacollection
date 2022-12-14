from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('',views.shopHome, name='shophome'),
    path('category-list',views.categoryList, name='categorylist'),
    path('product-list',views.productList, name='productlist'),

    path('add-category',views.addCategory, name='addcategory'),
    path('add-subcategory/<int:id>',views.addSubCategory, name='addsubcategory'),
    path('add-product/<int:id>',views.addProduct, name='addproduct'),

    path('new-arrivals',views.newArrivals, name='newarrivals'),
    path('hot-deal-products',views.hotDealProducts, name='hotdealproducts'),
    path('social-media',views.socialMediaLinks, name='socialmedialink'),
    path('banner',views.banner, name='banner'),
]