from django.shortcuts import render, redirect
from website.models import BreakingNews, AdminHomeBanner, AdminNewArrivalBanner, AdminProductBanner, CartId, CartItems, Category, HotDealPrice, Products, RestoSave, Shop, ShopNewArrivalBanner, ShopProductBanner, ShopSocialMediaLinks, Subcategory, ShopSliderBanner, ShopHomeBanner

from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum

from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def _rest_id(request):
    cuser = request.session.session_key
    if not cuser:
        cuser = request.session.create()
    return cuser


# hHOME
def collectionHome(request,id):
    shop_obj = Shop.objects.get(id=id)
    category_list = Products.objects.select_related('subcategory').filter(subcategory__category__shop=shop_obj).values("subcategory__category__name", "subcategory__category__icon", "subcategory__category__id").distinct() 
    category_looping = Category.objects.filter(shop=shop_obj)
    social_link = ShopSocialMediaLinks.objects.get(shop=shop_obj)
    slider = ShopSliderBanner.objects.filter(shop=shop_obj).order_by('-id')[:2]
    shophome_banner = ShopHomeBanner.objects.filter(shop=shop_obj).order_by('-id')[:2]
    if AdminHomeBanner:
        banner_status = 1
        home_banner = AdminHomeBanner.objects.all().last()
    else :
        banner_status = 2
        home_banner = ""
    if BreakingNews.objects.filter(shop__id=shop_obj.id).exists():
        news = BreakingNews.objects.filter(shop=shop_obj).last()
        latest_news = news.news
    else:
        latest_news = "............ Coming soon ..........."
    if RestoSave.objects.filter(user_session_id=_rest_id(request), resto_pk=id).exists():
        resto_save = RestoSave.objects.get(user_session_id=_rest_id(request), resto_pk=id)
    else:
        resto_save = RestoSave.objects.create(user_session_id=_rest_id(request), resto_pk=id)
        resto_save.save()
    context = {
        "is_home":True,
        'status':banner_status,
        'home_banner':home_banner,
        'category_list':category_list,
        "category_looping":category_looping,
        "shop_obj":shop_obj,
        "social_link":social_link,
        "news":latest_news,
        "sliders":slider,
        "shophome_banner":shophome_banner,
    }
    return render(request, 'collection/home.html', context)


# SUBCATEGORY
def subCategory(request,id):
    subcatgory_list = Subcategory.objects.filter(category__id=id)
    shop_session = RestoSave.objects.filter(user_session_id=request.session.session_key).last()
    shop_obj = Shop.objects.get(id=shop_session.resto_pk)
    category_looping = Category.objects.filter(shop=shop_obj)
    social_link = ShopSocialMediaLinks.objects.get(shop=shop_obj)
    if BreakingNews.objects.filter(shop__id=shop_obj.id).exists():
        news = BreakingNews.objects.filter(shop=shop_obj).last()
        latest_news = news.news
    else:
        latest_news = "............ Coming soon ..........."
    if AdminProductBanner:
        banner_status = 1
        product_banner = AdminProductBanner.objects.all().last()
    else :
        banner_status = 2
        product_banner = ""
    context = {
        "is_home":True,
        "status":banner_status,
        "product_banner":product_banner,
        'subcatgory_list':subcatgory_list,
        "category_looping":category_looping,
        "shop_obj":shop_obj,
        "social_link":social_link,
        "news":latest_news
    }
    return render(request, 'collection/subcategory.html', context)


def products(request,id):
    product_list = Products.objects.filter(subcategory__id=id)
    shop_session = RestoSave.objects.filter(user_session_id=request.session.session_key).last()
    shop_obj = Shop.objects.get(id=shop_session.resto_pk)
    category_looping = Category.objects.filter(shop=shop_obj)
    social_link = ShopSocialMediaLinks.objects.get(shop=shop_obj)
    if ShopProductBanner:
        banners_status = 1
        shopproduct_banner = ShopProductBanner.objects.all().last()
    else :
        banners_status = 2
        shopproduct_banner = ""
    if BreakingNews.objects.filter(shop__id=shop_obj.id).exists():
        news = BreakingNews.objects.filter(shop=shop_obj).last()
        latest_news = news.news
    else:
        latest_news = "............ Coming soon ..........."
    context = {
        "is_product":True,
        'product_list':product_list,
        "category_looping":category_looping,
        "shop_obj":shop_obj,
        "social_link":social_link,
        "news":latest_news,
        "shopproduct_banner":shopproduct_banner,
        "banners_status":banners_status,
    }
    return render(request, 'collection/product.html', context)


def productDetails(request,id):
    product_details = Products.objects.get(id=id)
    shop_session = RestoSave.objects.filter(user_session_id=request.session.session_key).last()
    shop_obj = Shop.objects.get(id=shop_session.resto_pk)
    category_looping = Category.objects.filter(shop=shop_obj)
    social_link = ShopSocialMediaLinks.objects.get(shop=shop_obj)
    if BreakingNews.objects.filter(shop__id=shop_obj.id).exists():
        news = BreakingNews.objects.filter(shop=shop_obj).last()
        latest_news = news.news
    else:
        latest_news = "............ Coming soon ..........."
    context = {
        "is_product_details":True,
        'product_details':product_details,
        "category_looping":category_looping,
        "shop_obj":shop_obj,
        "social_link":social_link,
        "news":latest_news
    }
    return render(request, 'collection/product-details.html', context)


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def AddToCart(request, pid, qty):
    product = Products.objects.get(id=pid)
    size = request.GET['size']
    try:
        cart = CartId.objects.get(cart_id=_cart_id(request))
    except CartId.DoesNotExist:
        cart = CartId.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        cart_item = CartItems.objects.get(product=product, cart=cart, size=size)
        cart_item.quantity = cart_item.quantity + qty
        cart_item.save()
        cart_item.size = size
        cart_item.save()
        total_price = float(cart_item.quantity) * float(product.price)
        cart_item.total = total_price
        cart_item.save()
        cart.save()
        messages.success(request, 'Successfully Add item to cart')
    except CartItems.DoesNotExist:
        cart_item = CartItems.objects.create(product=product, quantity=qty, cart=cart, size=size)
        cart_item.save()
        cart_item.size = size
        total_price = int(qty) * float(product.price)
        cart_item.total = total_price
        cart_item.save()
        cart.save()
        messages.success(request, 'Successfully Add item to cart')
    return redirect("/collection/product-details/"+str(product.id))


def cart(request):
    cart_item = CartItems.objects.filter(cart__cart_id=_cart_id(request))
    sub_total = CartItems.objects.filter(cart__cart_id=_cart_id(request)).aggregate(Sum("total"))
    shop_session = RestoSave.objects.filter(user_session_id=request.session.session_key).last()
    shop_obj = Shop.objects.get(id=shop_session.resto_pk)
    category_looping = Category.objects.filter(shop=shop_obj)
    social_link = ShopSocialMediaLinks.objects.get(shop=shop_obj)
    if BreakingNews.objects.filter(shop__id=shop_obj.id).exists():
        news = BreakingNews.objects.filter(shop=shop_obj).last()
        latest_news = news.news
    else:
        latest_news = "............ Coming soon ..........."
    context = {
        "is_cart":True,
        'cart_item':cart_item,
        'sub_total':sub_total,
        "category_looping":category_looping,
        "shop_obj":shop_obj,
        "social_link":social_link,
        "news":latest_news
    }
    return render(request, 'collection/cart.html', context)


@csrf_exempt
def addquantity(request):
    quantity = request.GET["quantity"]
    id = request.GET["id"]
    cart_obj = CartItems.objects.get(id=id)
    new_quantity = int(quantity) 
    product_total = float(new_quantity) * float(cart_obj.product.price)
    cart_obj.total = product_total
    cart_obj.save()
    gtotal = CartItems.objects.filter(cart__cart_id=request.session.session_key).aggregate(Sum('total'))
    CartItems.objects.filter(id=id).update(quantity=new_quantity, total=product_total)
    data = {"total": cart_obj.total, "unitprice": cart_obj.product.price, 'gtotal':gtotal["total__sum"],}

    return JsonResponse(data)


def checkout(request):
    cart_item = CartItems.objects.filter(cart__cart_id=_cart_id(request))
    grand_total = CartItems.objects.filter(cart__cart_id=_cart_id(request)).aggregate(Sum("total"))
    shop_session = RestoSave.objects.filter(user_session_id=request.session.session_key).last()
    shop_obj = Shop.objects.get(id=shop_session.resto_pk)
    category_looping = Category.objects.filter(shop=shop_obj)
    social_link = ShopSocialMediaLinks.objects.get(shop=shop_obj)
    if BreakingNews.objects.filter(shop__id=shop_obj.id).exists():
        news = BreakingNews.objects.filter(shop=shop_obj).last()
        latest_news = news.news
    else:
        latest_news = "............ Coming soon ..........."
    context = {
        "is_checkout":True,
        'cart_item':cart_item,
        'grand_total':grand_total,
        "category_looping":category_looping,
        "shop_obj":shop_obj,
        "social_link":social_link,
        "news":latest_news
    }
    return render(request, 'collection/checkout.html',context)


@csrf_exempt
def customerCheckout(request):
    first_name = request.POST['fisrtname']
    last_name = request.POST['lastname']
    phone = request.POST['phone']
    email = request.POST['email']
    messagestring = ""
    cart_obj = CartId.objects.get(cart_id=_cart_id(request))
    cart_items = CartItems.objects.filter(cart=cart_obj)
    shopcart_obj = CartItems.objects.filter(cart=cart_obj).last()
    shop_obj = ShopSocialMediaLinks.objects.filter(shop=shopcart_obj.product.subcategory.category.shop).last()
    shop_number = shop_obj.whatsapp
    sub_total = CartItems.objects.filter(cart__cart_id=_cart_id(request)).aggregate(Sum("total"))
    data = []
    try:
        messagestring = "https://wa.me/+91" + shop_number + "?text=First Name :" + first_name + "?text=Last Name :" + last_name  + "?text=Phone:" + phone + "?text=Email:" + email + "%0a------Order Details------"
        for i in cart_items:
            data1 = {
                "Product-Id":i.product.product_id,
                "Product-name": i.product.name,
                "quantity": i.quantity,
                "size":i.size,
                "price": i.product.price,
                "sub_total": i.total,
            }
            data.append(data1)
            i.delete()
        for j in data:
            messagestring += (
                "%0aProduct-Id:"
                + str(j["Product-Id"])
                + "%0aProduct-Name:"
                + str(j["Product-name"])
                + "%0aQuantity:"
                + str(j["quantity"])
                + "%0aSize:"
                + str(j["size"])
                + "%0aUnit-Price:"
                + str(j["price"])
                + "%0aTotal :"
                + str(j["sub_total"])
                + "%0a-----------------------------"
            )
            messagestring += "%0a-----------------------------"
        messagestring += (
            "%0a-----------------------------\
        Grand Total :"
            + str(sub_total["total__sum"])
            + "%0a-----------------------------"
        )
        cart_obj.delete()
    except Exception:
        pass
    print(messagestring)
    data = {
        "link":messagestring,
    }
    return JsonResponse(data)


def orderSuccess(request):
    return render(request, 'collection/order_success.html')


def newArrivals(request):
    shops = RestoSave.objects.filter(user_session_id=request.session.session_key).last()
    new_arrivals = Products.objects.filter(is_new_arrival=True, subcategory__category__shop__id=shops.resto_pk)
    shop_obj = Shop.objects.get(id=shops.resto_pk)
    social_link = ShopSocialMediaLinks.objects.get(shop=shop_obj)
    category_looping = Category.objects.filter(shop=shop_obj)
    if BreakingNews.objects.filter(shop__id=shop_obj.id).exists():
        news = BreakingNews.objects.filter(shop=shop_obj).last()
        latest_news = news.news
    else:
        latest_news = "............ Coming soon ..........."
    if AdminNewArrivalBanner:
        banner_status = 1
        arrival_banner = AdminNewArrivalBanner.objects.all().last()
    else :
        banner_status = 2
        arrival_banner = ""
    if ShopNewArrivalBanner:
        newbanners_status = 1
        shopnew_banner = ShopNewArrivalBanner.objects.all().last()
    else :
        newbanners_status = 2
        shopnew_banner = ""
    context = {
        "is_new":True,
        'status':banner_status,
        "new_banner":arrival_banner,
        "new_arrivals":new_arrivals,
        "category_looping":category_looping,
        "shop_obj":shop_obj,
        "social_link":social_link,
        "news":latest_news,
        "newbanners_status":newbanners_status,
        "shopnew_banner":shopnew_banner,
    }
    return render(request, 'collection/new_arrivals.html', context)


def hotdeals(request):
    shops = RestoSave.objects.filter(user_session_id=request.session.session_key).last()
    hot_deals = HotDealPrice.objects.filter(product__subcategory__category__shop__id=shops.resto_pk)
    shop_obj = Shop.objects.get(id=shops.resto_pk)
    
    context = {
        "hot_deals":hot_deals,
        "shop_obj":shop_obj,
    }
    return render(request, 'collection/hotdeals.html', context)


@csrf_exempt
def contact(request):
    shop_session = RestoSave.objects.filter(user_session_id=request.session.session_key).last()
    shop_obj = Shop.objects.get(id=shop_session.resto_pk)
    category_looping = Category.objects.filter(shop=shop_obj)
    social_objects = ShopSocialMediaLinks.objects.filter(shop=shop_obj).last()
    shop_number = social_objects.whatsapp
    social_link = ShopSocialMediaLinks.objects.get(shop=shop_obj)
    if BreakingNews.objects.filter(shop__id=shop_obj.id).exists():
        news = BreakingNews.objects.filter(shop=shop_obj).last()
        latest_news = news.news
    else:
        latest_news = "............ Coming soon ..........."
    context = {
        "is_contact":True,
        "category_looping":category_looping,
        "shop_obj":shop_obj,
        "social_link":social_link,
        "news":latest_news
    }
    return render(request, 'collection/contact.html', context)


@csrf_exempt
def contactData(request):
    shop_session = RestoSave.objects.filter(user_session_id=request.session.session_key).last()
    shop_obj = Shop.objects.get(id=shop_session.resto_pk)
    social_objects = ShopSocialMediaLinks.objects.filter(shop=shop_obj).last()
    shop_number = social_objects.whatsapp
    first_name = request.POST['firstname']
    print(first_name,'1'*7)
    last_name = request.POST['lastname']
    phone = request.POST['phone']
    email = request.POST['email']
    address = request.POST['address']
    messagestring = "https://wa.me/+91" + shop_number + "?text=First Name :" + first_name + "?text=Last Name :" + last_name  + "?text=Phone:" + phone + "?text=Email:" + email + "?text=Address:" + address + "%0a------Order Details------"
    data = {
        "link":messagestring
    }
    return JsonResponse(data)