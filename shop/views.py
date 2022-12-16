import datetime
from django.shortcuts import render, redirect

from website.models import Category, HotDealPrice, Products, ShopQrcode, ShopSocialMediaLinks, Subcategory
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse

# Create your views here.


def shopHome(request):
    user = request.user
    qr_code = ShopQrcode.objects.get(shop=user.shop)
    social_media = ShopSocialMediaLinks.objects.get(shop=user.shop)
    category_count = Category.objects.filter(shop=user.shop).count()
    product_count = Products.objects.filter(subcategory__category__shop=user.shop).count()
    hotdeal_count = HotDealPrice.objects.filter(product__subcategory__category__shop=user.shop).count()
    new_arrival_count = Products.objects.filter(subcategory__category__shop=user.shop, is_new_arrival=True).count()
    five_products = Products.objects.filter(subcategory__category__shop=user.shop)[:5]
    print(social_media)
    context = {
        "is_home":True,
        "qr_code":qr_code,
        "social_media":social_media,
        "category_count":category_count,
        "product_count":product_count,
        "hotdeal_count":hotdeal_count,
        "new_arrival_count":new_arrival_count,
        "five_products":five_products,
    }
    return render(request, 'shop/home.html',context)


def categoryList(request):
    # all_categories = Category.objects.filter(shop=request.user.shop)
    all_categories = Products.objects.select_related('subcategory__category').filter(subcategory__category__shop=request.user.shop).values('subcategory__category__name','subcategory__category__id').annotate(count=Count('id')).distinct()
    context = {
        'is_list':True,
        'all_categories':all_categories
    }
    return render(request, 'shop/category_list.html', context)


def subcategoryList(request,id):
    all_subcategories = Products.objects.select_related('subcategory').filter(subcategory__category__shop=request.user.shop, subcategory__category__id=id).values('subcategory__name','subcategory__id').annotate(count=Count('id')).distinct()
    context = {
        'is_list':True,
        'all_subcategories':all_subcategories
    }
    return render(request, 'shop/subcategory_list.html', context)


def productList(request,id):
    all_products = Products.objects.filter(subcategory__category__shop=request.user.shop, subcategory__id=id)
    if request.method == 'POST':
        pname = request.POST['h-name']
        pid = request.POST['pk']
        product_object = Products.objects.get(id=pid)
        price = request.POST['h-price']
        date = datetime.datetime.now()
        if HotDealPrice.objects.filter(product=product_object).exists():
            HotDealPrice.objects.filter(product=product_object).update(price=price, date=date)
            return redirect('/shop/product-list/'+str(id))
        else:
            hot_price = HotDealPrice(product=product_object, price=price)
            hot_price.save()
            return redirect('/shop/product-list/'+str(id))
    context = {
        'is_list':True,
        'all_products':all_products
    }
    return render(request, 'shop/product_list.html', context)


def addToNewArrivals(request, id):
    new = Products.objects.get(id=id)
    if  new.is_new_arrival == False:
        new.is_new_arrival=True
        new.save()
        return redirect('/shop/product-list/'+str(new.subcategory.id))
    else:
        new.is_new_arrival=False
        new.save()
        return redirect('/shop/product-list/'+str(new.subcategory.id))


def getProductData(request,id):
    product_details = Products.objects.get(id=id)
    try:
        hotdeal_obj = HotDealPrice.objects.get(product=product_details)
        hot_deal_price = hotdeal_obj.price
    except:
        hot_deal_price = 0
    print(product_details, '*'*10)
    data = {
        'product_name':product_details.name,
        'id':product_details.id,
        'hot_deal_price':hot_deal_price
    }
    return JsonResponse(data)



def addCategory(request):
    if request.method == 'POST':
        category_name = request.POST['category-name'] 
        category_image = request.FILES['category-image']
        new_category = Category(name=category_name, icon=category_image, shop=request.user.shop)
        new_category.save()
        messages.success(request, 'Category added successfully')
    all_categories = Category.objects.filter(shop=request.user.shop)
    context = {
        'is_add':True,
        'all_categories':all_categories
    }
    return render(request, 'shop/add_category.html', context)


def addSubCategory(request, id):
    category_id = Category.objects.get(id=id)
    if request.method == 'POST':
        subcategory_name = request.POST['subcategory-name'] 
        subcategory_image = request.FILES['subcategory-image']
        new_subcategory = Subcategory(name=subcategory_name, icon=subcategory_image, category=category_id)
        new_subcategory.save()
        messages.success(request, 'Category added successfully')
    all_subcategories = Subcategory.objects.filter(category__shop=request.user.shop,category=category_id)
    context = {
        'is_add':True,
        'all_subcategories':all_subcategories
    }
    return render(request, 'shop/add_subcategory.html', context)


def addProduct(request, id):
    subcategory_id = Subcategory.objects.get(id=id)
    if Products.objects.exists():
        product = Products.objects.last().id
        product_id = 'abc'+str(100+product)
    else:
        prd = 0
        product_id = 'abc'+str(100+prd)
    if request.method == 'POST':
        now = datetime.datetime.now()
        product_id = product_id  
        product_name = request.POST['p_name'] 
        price = request.POST['p_price'] 
        sizes = request.POST['p_size']
        description = request.POST['p_descriptions']
        product_details = request.POST['p_details']
        image = request.FILES['p_image']
        if not Products.objects.filter(name=product_name).exists():
            try:
                # new_arrivals = request.POST['new_arrivals']
                new_product = Products(subcategory=subcategory_id, product_id=product_id, name=product_name, price=price, size=sizes, description=description, product_details=product_details, image=image, date=now,is_new_arrival=True,)
                new_product.save()
                return redirect('/shop/add-product/'+str(subcategory_id.id))
            except:
                new_product = Products(subcategory=subcategory_id, product_id=product_id, name=product_name, price=price, size=sizes, description=description, product_details=product_details, image=image, is_new_arrival=False, date=now)
                new_product.save()
                return redirect('/shop/add-product/'+str(subcategory_id.id))
    all_product = Products.objects.filter(subcategory__category__shop=request.user.shop, subcategory=subcategory_id)
    context = {
        'is_add':True,
        'all_product':all_product
    }
    return render(request, 'shop/add_product.html', context)


def newArrivals(request):
    new_arrivals = Products.objects.filter(subcategory__category__shop=request.user.shop, is_new_arrival=True)
    context = {
        'is_new':True,
        'new_arrivals':new_arrivals
    }
    return render(request, 'shop/new_arrivals.html', context)



def hotDealProducts(request):
    hot_deal_products = HotDealPrice.objects.filter(product__subcategory__category__shop=request.user.shop)
    if request.method == 'POST':
        pname = request.POST['h-name']
        pid = request.POST['pk']
        product_object = Products.objects.get(id=pid)
        price = request.POST['h-price']
        date = datetime.datetime.now()
        if HotDealPrice.objects.filter(product=product_object).exists():
            HotDealPrice.objects.filter(product=product_object).update(price=price, date=date)
            return redirect('shop:hotdealproducts')
        else:
            hot_price = HotDealPrice(product=product_object, price=price)
            hot_price.save()
            return redirect('shop:hotdealproducts')
    context = {
        'is_hot':True,
        'hot_deal_products':hot_deal_products
    }
    return render(request, 'shop/hot_deal.html',context)


def deleteHotDeal(request,id):
    HotDealPrice.objects.get(id=id).delete()
    return redirect('shop:hotdealproducts')


def socialMediaLinks(request):
    if request.method == 'POST':
        facebook = request.POST['facebook']
        instagram = request.POST['instagram']
        whatsapp = request.POST['whatsapp']
        location = request.POST['location']
        number = request.POST['number']
        if ShopSocialMediaLinks.objects.filter(shop=request.user.shop).exists():
            ShopSocialMediaLinks.objects.filter(shop=request.user.shop).update(facebook=facebook, whatsapp=whatsapp, instagram=instagram, location=location, phone_number=number)
        else:
            new_link = ShopSocialMediaLinks(shop=request.user.shop, facebook=facebook, whatsapp=whatsapp, instagram=instagram, location=location, phone_number=number)
            new_link.save()
    if ShopSocialMediaLinks.objects.filter(shop=request.user.shop).exists():
        links = ShopSocialMediaLinks.objects.get(shop=request.user.shop)
        context = {
            "links":links
        }
        return render(request, 'shop/social_media.html',context)
    else:
        print('else')
        pass
    context = {
        'is_social':True,
    }
    return render(request, 'shop/social_media.html', context)


def banner(request):
    context = {
        'is_banner':True,
    }
    return render(request, 'shop/banner.html', context)


def profile(request):
    profile = request.user.shop
    context = {
        'is_profile':True,
        'profile':profile
    }
    return render(request, 'shop/profile.html', context)
