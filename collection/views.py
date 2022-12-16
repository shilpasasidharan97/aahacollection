from django.shortcuts import render

from website.models import Products, Shop, Subcategory


# Create your views here.


def collectionHome(request,id):
    shop_obj = Shop.objects.get(id=id)
    category_list = Products.objects.select_related('subcategory').filter(subcategory__category__shop=shop_obj).values("subcategory__category__name", "subcategory__category__icon", "subcategory__category__id").distinct() 
    context = {
        'category_list':category_list
    }
    return render(request, 'collection/home.html', context)



def subCategory(request,id):
    subcatgory_list = Subcategory.objects.filter(category__id=id)
    context = {
        'subcatgory_list':subcatgory_list
    }
    return render(request, 'collection/subcategory.html', context)


def products(request,id):
    product_list = Products.objects.filter(subcategory__id=id)
    context = {
        'product_list':product_list
    }
    return render(request, 'collection/product.html', context)


def productDetails(request,id):
    product_details = Products.objects.get(id=id)
    print(product_details)
    context = {
        'product_details':product_details
    }
    return render(request, 'collection/product-details.html', context)


def cart(request):
    return render(request, 'collection/cart.html')


def checkout(request):
    return render(request, 'collection/checkout.html')


def orderSuccess(request):
    return render(request, 'collection/order_success.html')


def contact(request):
    return render(request, 'collection/contact.html')