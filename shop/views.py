from django.shortcuts import render

# Create your views here.


def shopHome(request):
    return render(request, 'shop/home.html')


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
    return render(request, 'shop/social_media.html')


def banner(request):
    return render(request, 'shop/banner.html')
