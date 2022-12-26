from website.models import CartItems
from django.db.models import Sum


def main_context(request):
    if request.session.exists(request.session.session_key):
        cart_items = CartItems.objects.filter(cart__cart_id=request.session.session_key)
        grand_total = CartItems.objects.filter(cart__cart_id=request.session.session_key).aggregate(Sum("total"))
        return {
            "domain": request.META["HTTP_HOST"],
            "cart_items": cart_items,
            "grand_total":grand_total,
        }
    else:
        return {"domain": request.META["HTTP_HOST"]}

