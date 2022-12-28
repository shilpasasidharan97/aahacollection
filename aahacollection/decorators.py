from django.shortcuts import redirect


def auth_shop(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        try:
            if user is not None:
                if user.shop:
                    return func(request, *args, **kwargs)
                else:
                    return redirect("official:loginpage")
            else:
                return redirect("official:loginpage")
        except:
            return redirect("official:loginpage")
    return wrap


def auth_official(func):
    def wrap(request, *args, **kwargs):
        shop_ex = request.user
        if shop_ex is not None:
            if shop_ex.is_superuser:
                return func(request, *args, **kwargs)
            else:
                return redirect("official:loginpage")
        else:
            return redirect("official:loginpage")

    return wrap
