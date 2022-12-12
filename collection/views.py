from django.shortcuts import render


# Create your views here.


def collectionHome(request):
    return render(request, 'collection/home.html')



def subCategory(request):
    return render(request, 'collection/subcategory.html')


def products(request):
    return render(request, 'collection/product.html')


def productDetails(request):
    return render(request, 'collection/product-details.html')


def cart(request):
    return render(request, 'collection/cart.html')


def checkout(request):
    return render(request, 'collection/checkout.html')