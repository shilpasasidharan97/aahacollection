

from official.models import *
from website.models import User


def main_context(request):
    if request.session.exists(request.session.session_key):
        # shops = request.user.shop
        # try :
        #     shops = request.user.shop
        # except :
        #     shops = ""
        #     pass
        # print(shops,'hello')
        if User.objects.filter(is_staff=True).exists():
            # shops = request.user.shop
            # pickUpBoy = PickUpBoy.objects.get(id=request.user.pickup_boy.id)
            return {
                "domain": request.META["HTTP_HOST"],
                # "shops":shops
            }
        else:
            return {
                "domain": request.META["HTTP_HOST"],
            }
    else:
        return {
            "domain": request.META["HTTP_HOST"],
        }