from django.contrib import admin

from website.models import Shop, ShopQrcode, ShopSocialMediaLinks, User

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