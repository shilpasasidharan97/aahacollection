from django.shortcuts import render, redirect

from website.models import CartId, CartItems, Products, Shop, Subcategory

from django.http import JsonResponse
from django.contrib import messages


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


def _cart_id(request):
#     cart = request.session.session_key
#     if not cart:
#         cart = request.session.create()
    return cart


def AddToCart(request, pid, qty):
    product = Products.objects.get(id=pid)
    try:
        cart = CartId.objects.get(cart_id=_cart_id(request))
    except CartId.DoesNotExist:
        cart = CartId.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        cart_item = CartItems.objects.get(product=product, cart=cart)
        cart_item.quantity = cart_item.quantity + qty
        cart_item.save()
        total_price = float(cart_item.quantity) * float(product.price)
        cart_item.total = total_price
        cart_item.save()
        cart.save()
        messages.success(request, 'Successfully Add item to cart')
    except CartItems.DoesNotExist:
        cart_item = CartItems.objects.create(product=product, quantity=qty, cart=cart)
        cart_item.save()
        total_price = int(qty) * float(product.price)
        cart_item.total = total_price
        cart_item.save()
        cart.save()
        messages.success(request, 'Successfully Add item to cart')
    return redirect("/collection/product-details/"+str(product.id))


# def addQuantity(request):
#     # quantity = request.GET["quantity"]
#     # id = request.GET["id"]
#     # cart_obj = CartItems.objects.get(id=id)
#     # new_quantity = int(quantity) + 1
#     # product_total = float(new_quantity) * float(cart_obj.product.price)
#     # cart_obj.total = product_total
#     # cart_obj.save()
#     # CartItems.objects.filter(id=id).update(quantity=new_quantity, total=product_total)
#     # data = {"total": cart_obj.total, "unitprice": cart_obj.product.price}
#     return JsonResponse({'data':'data',})


# def lessQuantity(request):
#     quantity = request.GET["quantity"]
#     id = request.GET["id"]
#     # cart_obj = CartItems.objects.get(id=id)
#     # new_quantity = int(quantity) - 1
#     # # product_total = float(new_quantity) * float(cart_obj.product.price)
#     # # cart_obj.total = product_total
#     # # cart_obj.save()
#     # CartItems.objects.filter(id=id).update(quantity=new_quantity, total=product_total)
#     # data = {"total": cart_obj.total, "unitprice": cart_obj.product.price}
#     return JsonResponse({'data':'data',})


def cart(request):
    return render(request, 'collection/cart.html')


def checkout(request):
    return render(request, 'collection/checkout.html')


def orderSuccess(request):
    return render(request, 'collection/order_success.html')


def contact(request):
    return render(request, 'collection/contact.html')