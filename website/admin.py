from django.contrib import admin

from website.models import Category, Products, Shop, ShopQrcode, ShopSocialMediaLinks, Subcategory, User

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


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','shop','name','icon')
    search_fields=('shop', 'name')
admin.site.register(Category,CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category','name','icon')
    search_fields=('category', 'name')
admin.site.register(Subcategory,SubcategoryAdmin)


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id','price','size','is_new_arrival', 'subcategory')
    search_fields=('product_id','price',)
admin.site.register(Products,ProductsAdmin)