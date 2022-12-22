from website.models import CartItems


def main_context(request):
    if request.session.exists(request.session.session_key):
        cart_items = CartItems.objects.filter(cart__cart_id=request.session.session_key)
        print('cartitem'*20)
        return {
            "domain": request.META["HTTP_HOST"],
            "cart_items": cart_items,
        }
    else:
        print('not working')
        return {"domain": request.META["HTTP_HOST"]}

