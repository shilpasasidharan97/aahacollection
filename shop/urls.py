from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('',views.shopHome, name='shophome'),
    path('category-list',views.categoryList, name='categorylist'),
    path('subcategory-list/<int:id>',views.subcategoryList, name='subcategorylist'),
    path('product-list/<int:id>',views.productList, name='productlist'),

    path('add-category',views.addCategory, name='addcategory'),
    path('add-subcategory/<int:id>',views.addSubCategory, name='addsubcategory'),
    path('add-product/<int:id>',views.addProduct, name='addproduct'),

    path('new-arrivals/',views.newArrivals, name='newarrivals'),

    path('add-to-newarrivals/<int:id>', views.addToNewArrivals, name='addtonewarrivals'),
    path('getproductdata/<int:id>',views.getProductData, name='getproductdata'),


    path('hot-deal-products/',views.hotDealProducts, name='hotdealproducts'),
    path('delete-deal/<int:id>',views.deleteHotDeal, name='deletedeal'),

    path('social-media/',views.socialMediaLinks, name='socialmedialink'),
    path('banner',views.banner, name='banner'),

    path('profile',views.profile, name='profile'),
]