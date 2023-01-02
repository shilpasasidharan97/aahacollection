from django.contrib import admin

from website.models import AdminData, BreakingNews, AdminHomeBanner, AdminNewArrivalBanner, AdminProductBanner, AdminSocialMediaLinks, CartItems, Category, HotDealPrice, Products, RestoSave, Shop, ShopHomeBanner, ShopNewArrivalBanner, ShopProductBanner, ShopQrcode, ShopSliderBanner, ShopSocialMediaLinks, Subcategory, User


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','phone')
    search_fields=('phone',)
admin.site.register(User,UserAdmin)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id','shop_name','email','phone','password','date')
    search_fields=('phone',)
admin.site.register(Shop,ShopAdmin)


class ShopQrcodeAdmin(admin.ModelAdmin):
    list_display = ('shop','resto_url','image')
    search_fields=('shop',)
admin.site.register(ShopQrcode,ShopQrcodeAdmin)


class ShopSocialMediaLinksAdmin(admin.ModelAdmin):
    list_display = ('shop','facebook','phone_number')
    search_fields=('shop',)
admin.site.register(ShopSocialMediaLinks,ShopSocialMediaLinksAdmin)


class AdminSocialMediaLinksAdmin(admin.ModelAdmin):
    list_display = ('facebook','phone_number')
    search_fields=()
admin.site.register(AdminSocialMediaLinks,AdminSocialMediaLinksAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','shop','name','icon')
    search_fields=('shop', 'name')
admin.site.register(Category,CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category','name','icon')
    search_fields=('category', 'name')
admin.site.register(Subcategory,SubcategoryAdmin)


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id','name', 'price','size','is_new_arrival', 'subcategory')
    search_fields=('product_id','price',)
admin.site.register(Products,ProductsAdmin)


class HotDealPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price',)
    search_fields=('product','price',)
admin.site.register(HotDealPrice,HotDealPriceAdmin)


class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'total', 'size' )
    search_fields=('product','quantity', 'total', )
admin.site.register(CartItems,CartItemsAdmin)

class AdminHomeBannerAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields=('banner',)
admin.site.register(AdminHomeBanner,AdminHomeBannerAdmin)

class AdminNewArrivalBannerAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields=('banner',)
admin.site.register(AdminNewArrivalBanner,AdminNewArrivalBannerAdmin)


class AdminProductBannerAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields=('banner',)
admin.site.register(AdminProductBanner,AdminProductBannerAdmin)

admin.site.register(RestoSave)
admin.site.register(BreakingNews)
admin.site.register(ShopSliderBanner)
admin.site.register(ShopHomeBanner)
admin.site.register(ShopNewArrivalBanner)
admin.site.register(ShopProductBanner)
admin.site.register(AdminData)

