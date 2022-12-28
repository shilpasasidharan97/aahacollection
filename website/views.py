from django.shortcuts import render, redirect

from django.utils import timezone
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login

from website.models import Shop, ShopQrcode, ShopSocialMediaLinks

# Create your views here.


def websiteHome(request):
    return render(request, 'website/home.html')

def registration(request):
    if request.method == 'POST':
        shop_name = request.POST['shop_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        place = request.POST['place']
        district = request.POST['district']
        state = request.POST['state']
        password = request.POST['password']
        c_password = request.POST['c_password']
        shoplogo = request.FILES['shoplogo']
        address = request.POST['address']
        date = datetime.datetime.now()
        if password == c_password:
            if not Shop.objects.filter(phone=phone_number).exists():
                new_shop = Shop(shop_name=shop_name,email=email,phone=phone_number,place=place,district=district,state=state,address=address,password=password,logo=shoplogo,date=date)
                new_shop.save()
                User = get_user_model()
                User.objects.create_user(phone=phone_number, password=password,email=email,shop=new_shop)
                user = authenticate(request,phone=phone_number,password=password)
                url = "https://aahacollections.geany.website/collection/collection/"+str(new_shop.id)
                # url = "http://127.0.0.1:9000/collection/collection/"+str(new_shop.id)
                ShopQrcode.objects.create(shop=new_shop,resto_url=url)
                links = ShopSocialMediaLinks(shop=new_shop, whatsapp=phone_number)
                links.save()
                if user is not None:
                    login(request, user)
                    return redirect('shop:shophome')
                else:
                    print("Not authenticated","*"*3)
    return render(request, 'website/registration.html')