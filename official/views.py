from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

# Create your views here.


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
            return redirect('official:loginpage')
    return render(request, 'official/login.html')


def logout_shop(request):
    logout(request)
    return redirect('official:loginpage')


def officialHome(request):
    return render(request, 'official/home.html')


def newUserRegistration(request):
    return render(request, 'official/new_user.html')


def customerList(request):
    return render(request, 'official/customer_list.html')


def banners(request):
    return render(request, 'official/banner.html')


def socialMedia(request):
    return render(request, 'official/social_medias.html')