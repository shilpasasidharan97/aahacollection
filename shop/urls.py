from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('',views.shopHome, name='shophome'),
    path('category-list',views.categoryList, name='categorylist'),
    path('subcategory-list/<int:id>',views.subcategoryList, name='subcategorylist'),
    path('product-list/<int:id>',views.productList, name='productlist'),

    path('add-category/',views.addCategory, name='addcategory'),
    path('get-category/<int:id>',views.getCategory, name='getcategory'),
    path('edit-category',views.editCategory, name='editcategory'),
    path('delete-category/<int:id>',views.deleteCategory, name='deletecatgory'),

    path('add-subcategory/<int:id>',views.addSubCategory, name='addsubcategory'),
    path('get-subcategory/<int:id>',views.getSubCategory, name='getsubcategory'),
    path('edit-subcategory',views.editSubCategory, name='editsubcategory'),
    path('delete-subcategory/<int:id>',views.deleteSubCategory, name='deletesubcatgory'),

    path('add-product/<int:id>',views.addProduct, name='addproduct'),
    path('view-product/<int:id>',views.viewProduct, name='view'),
    path('get-product/<int:id>',views.getProduct, name='getproduct'),
    path('edit-product',views.editProduct, name='editproduct'),
    path('delete-product/<int:id>',views.deleteProduct, name='delete'),

    # new arrival
    path('new-arrivals/',views.newArrivals, name='newarrivals'),
    path('remove-arrivals/<int:id>',views.removenewArrivals, name='removenewarrivals'),


    path('add-to-newarrivals/<int:id>', views.addToNewArrivals, name='addtonewarrivals'),
    path('getproductdata/<int:id>',views.getProductData, name='getproductdata'),


    path('hot-deal-products/',views.hotDealProducts, name='hotdealproducts'),
    path('delete-deal/<int:id>',views.deleteHotDeal, name='deletedeal'),

    path('social-media/',views.socialMediaLinks, name='socialmedialink'),

    path('banner/',views.banner, name='banner'),
    path('homebanner/',views.HomeBanner, name='homebanner'),
    path('product-banner/',views.ProductBanner, name='productbanner'),
    path('new-banner/',views.NewBanner, name='newbanner'),

    path('news',views.breakingNews, name='news'),

    path('profile',views.profile, name='profile'),
    path('settings',views.settings, name='settings'),
]