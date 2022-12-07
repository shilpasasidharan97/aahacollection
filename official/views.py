from django.shortcuts import render

# Create your views here.


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