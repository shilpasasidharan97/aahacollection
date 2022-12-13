from django.shortcuts import render

from website.models import ShopQrcode, ShopSocialMediaLinks

# Create your views here.


def shopHome(request):
    user = request.user
    qr_code = ShopQrcode.objects.get(shop=user.shop)
    social_media = ShopSocialMediaLinks.objects.get(shop=user.shop)
    context = {
        "is_home":True,
        "qr_code":qr_code,
        "social_media":social_media
    }
    return render(request, 'shop/home.html',context)


def categoryList(request):
    return render(request, 'shop/category_list.html')


def productList(request):
    return render(request, 'shop/product_list.html')


def addCategory(request):
    return render(request, 'shop/add_category.html')


def addProduct(request):
    return render(request, 'shop/add_product.html')


def newArrivals(request):
    return render(request, 'shop/new_arrivals.html')


def hotDealProducts(request):
    return render(request, 'shop/hot_deal.html')


def socialMediaLinks(request):
    if request.method == 'POST':
        facebook = request.POST['facebook']
        instagram = request.POST['instagram']
        whatsapp = request.POST['whatsapp']
        location = request.POST['location']
        number = request.POST['number']
        if ShopSocialMediaLinks.objects.filter(shop=request.user.shop).exists():
            ShopSocialMediaLinks.objects.filter(shop=request.user.shop).update(facebook=facebook, whatsapp=whatsapp, instagram=instagram, location=location, phone_number=number)
        else:
            new_link = ShopSocialMediaLinks(shop=request.user.shop, facebook=facebook, whatsapp=whatsapp, instagram=instagram, location=location, phone_number=number)
            new_link.save()
    if ShopSocialMediaLinks.objects.filter(shop=request.user.shop).exists():
        links = ShopSocialMediaLinks.objects.get(shop=request.user.shop)
        context = {
            "links":links
        }
        return render(request, 'shop/social_media.html',context)
    else:
        print('else')
        pass
    return render(request, 'shop/social_media.html')


def banner(request):
    return render(request, 'shop/banner.html')
