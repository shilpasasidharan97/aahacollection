from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from aahacollection.decorators import auth_official

from website.models import AdminData, AdminHomeBanner, AdminNewArrivalBanner, AdminProductBanner, AdminSocialMediaLinks, Shop, ShopQrcode, ShopSocialMediaLinks
import datetime
from django.contrib import messages

# Create your views here.


# LOGIN PAGE
def loginpage(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request,phone=phone, password=password)
        if user is not None:
            if user.shop:
                login(request, user)
                return redirect('shop:shophome')
            elif user.is_superuser == True:
                login(request, user)
                return redirect('official:officialhome')
            else:
                return redirect('official:loginpage')
        else:
            messages.success(request, 'Check your username or password')
            return redirect('official:loginpage')
    return render(request, 'official/login.html')


# LOGOUT
def logout_shop(request):
    logout(request)
    return redirect('official:loginpage')


# HOME
@login_required(login_url="/official/login-page")
@auth_official
def officialHome(request):
    twohome_banner = AdminHomeBanner.objects.all()[:2]
    if AdminSocialMediaLinks.objects.all().exists():
        social_media = AdminSocialMediaLinks.objects.all().last()
    else :
        social_media = AdminSocialMediaLinks.objects.create(user=request.user)
    five_shop = Shop.objects.all()[:5]
    all_shop_count = Shop.objects.all().count()
    context = {
        'is_home':True,
        'social_media':social_media,
        'all_shop_count':all_shop_count,
        'five_shop':five_shop,
        "twohome_banner":twohome_banner,
    }
    return render(request, 'official/home.html', context)


# NEW REGISTRATION
@login_required(login_url="/official/login-page")
@auth_official
def newUserRegistration(request):
    if request.method == 'POST':
        name = request.POST['s-name']
        email = request.POST['s-email']
        phone = request.POST['s-phone']
        city = request.POST['s-city']
        state = request.POST['s-state']
        district = request.POST['s-district']
        address = request.POST['s-address']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        now = datetime.datetime.now()
        if password == cpassword:
            if not Shop.objects.filter(phone=phone).exists():
                new_shop = Shop(shop_name=name,email=email,phone=phone,place=city,district=district,state=state,address=address,password=password,date=now)
                new_shop.save()
                User = get_user_model()
                User.objects.create_user(phone=phone, password=password,email=email,shop=new_shop)
                user = authenticate(request,phone=phone,password=password)
                # url = "https://aahamenu.geany.website/menucard/menucard/"+str(new_resto.id)
                url = "http://127.0.0.1:9000/collection/collection/"+str(new_shop.id)
                ShopQrcode.objects.create(shop=new_shop,resto_url=url)
                messages.success(request, 'Category added successfully')
                links = ShopSocialMediaLinks(shop=new_shop)
                links.save() 
    context = {
        'is_new':True,
    }    
    return render(request, 'official/new_user.html', context)


# CUSTOMER LIST
@login_required(login_url="/official/login-page")
@auth_official
def customerList(request):
    all_shops = Shop.objects.all().order_by('shop_name')
    context = {
        'all_shops':all_shops,
        'is_list':True,
    }
    return render(request, 'official/customer_list.html', context)


# BANNER
@login_required(login_url="/official/login-page")
@auth_official
def banners(request):
    all_home_banner = AdminHomeBanner.objects.all()
    all_prd_banner = AdminProductBanner.objects.all()
    all_new_banner = AdminNewArrivalBanner.objects.all()
    if request.method == "POST":
        product_image = request.FILES["home-image"]
        product_banner = AdminHomeBanner(banner=product_image)
        product_banner.save()
    context = {
        'is_banner':True,
        "all_home_banner":all_home_banner,
        "all_prd_banner":all_prd_banner,
        "all_new_banner":all_new_banner
    }
    return render(request, 'official/banner.html', context)


# product banner
def ProductBanner(request):
    if request.method == "POST":
        product_image = request.FILES["prd-image"]
        product_banner = AdminProductBanner(banner=product_image)
        product_banner.save()
    return redirect("official:banners")


# product banner
def NewBanner(request):
    if request.method == "POST":
        new_image = request.FILES["new-image"]
        new_banner = AdminNewArrivalBanner(banner=new_image)
        new_banner.save()
    return redirect("official:banners")


# SCOCIAL MEDIA
@login_required(login_url="/official/login-page")
@auth_official
def socialMedia(request):
    if request.method == 'POST':
        facebook = request.POST['facebook']
        instagram = request.POST['instagram']
        whatsapp = request.POST['whatsapp']
        location = request.POST['location']
        number = request.POST['number']
        email = request.POST['email']
        if AdminSocialMediaLinks.objects.filter(user=request.user).exists():
            AdminSocialMediaLinks.objects.filter(user=request.user).update(facebook=facebook, whatsapp=whatsapp, instagram=instagram, location=location, phone_number=number, email=email)
        else:
            new_link = AdminSocialMediaLinks(user=request.user, facebook=facebook, whatsapp=whatsapp, instagram=instagram, location=location, phone_number=number, email=email)
            new_link.save()
    if AdminSocialMediaLinks.objects.filter(user=request.user).exists():
        links = AdminSocialMediaLinks.objects.get(user=request.user)
        context = {
            "links":links,
            'is_social':True,
        }
        return render(request, 'official/social_medias.html',context)


# PROFILE
@login_required(login_url="/official/login-page")
@auth_official
def profile(request):
    data = AdminData.objects.all().last()
    context = {
        'is_profile':True,
        "data":data
    }
    return render(request, 'official/profile.html', context)


@auth_official
@login_required(login_url="/official/login-page")
def profiledata(request):
    if AdminData:
        admin_data = AdminData.objects.all().last()
    else:
        admin_data = AdminData.objects.create()
    if request.method == 'POST':
        name = request.POST['s-name']
        email = request.POST['s-email']
        phone = request.POST['s-phone']
        city = request.POST['s-city']
        state = request.POST['s-state']
        district = request.POST['s-district']
        address = request.POST['s-address']
            
        admin_data = AdminData(name=name,email=email,phone=phone,place=city,district=district,state=state,address=address)
        admin_data.save()
        messages.success(request, 'Added successfully')
        return redirect("official:profile")
    context = {
        'is_profile':True,
        "admin_data":admin_data
    }
    return render(request, 'official/profile_data.html', context)
