import datetime
from django.shortcuts import render, redirect

from website.models import Category, Products, ShopQrcode, ShopSocialMediaLinks, Subcategory
from django.contrib import messages

# Create your views here.


def shopHome(request):
    user = request.user
    qr_code = ShopQrcode.objects.get(shop=user.shop)
    social_media = ShopSocialMediaLinks.objects.get(shop=user.shop)
    context = {
        "is_home":True,
        "qr_code":qr_code,
        "social_media":social_media
    }
    return render(request, 'shop/home.html',context)


def categoryList(request):
    all_categories = Category.objects.filter(shop=request.user.shop)
    context = {
        'all_categories':all_categories
    }
    return render(request, 'shop/category_list.html', context)


def productList(request):
    return render(request, 'shop/product_list.html')


def addCategory(request):
    if request.method == 'POST':
        category_name = request.POST['category-name'] 
        category_image = request.FILES['category-image']
        new_category = Category(name=category_name, icon=category_image, shop=request.user.shop)
        new_category.save()
        messages.success(request, 'Category added successfully')
    all_categories = Category.objects.filter(shop=request.user.shop)
    context = {
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
                new_product = Products(subcategory=subcategory_id, product_id=product_id, name=product_name, price=price, size=sizes, description=description, product_details=product_details, image=image, date=now)
                new_product.save()
                return redirect('/shop/add-product/'+str(subcategory_id.id))
            except:
                new_product = Products(subcategory=subcategory_id, product_id=product_id, name=product_name, price=price, size=sizes, description=description, product_details=product_details, image=image, is_new_arrival=False, date=now)
                new_product.save()
                return redirect('/shop/add-product/'+str(subcategory_id.id))
    all_product = Products.objects.filter(subcategory__category__shop=request.user.shop, subcategory=subcategory_id)
    context = {
        'all_product':all_product
    }
    return render(request, 'shop/add_product.html', context)


def newArrivals(request):
    new_arrivals = Products.objects.filter(subcategory__category__shop=request.user.shop, is_new_arrival=True)
    context = {
        'new_arrivals':new_arrivals
    }
    return render(request, 'shop/new_arrivals.html', context)


def hotDealProducts(request):
    return render(request, 'shop/hot_deal.html')


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
    return render(request, 'shop/social_media.html')


def banner(request):
    return render(request, 'shop/banner.html')
