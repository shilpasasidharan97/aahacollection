from django.shortcuts import render

# Create your views here.


def collectionHome(request):
    return render(request, 'collection/home.html')


def products(request):
    return render(request, 'collection/product.html')