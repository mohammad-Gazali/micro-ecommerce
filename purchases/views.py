from django.shortcuts import get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from products.models import Product
from purchases.models import Purchase
from core.env import config
import stripe




STRIPE_PUBLIC_KEY = config("STRIPE_PUBLIC_KEY", default=None)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
SITE_URL = config("SITE_URL", default=None)


stripe.api_key = STRIPE_SECRET_KEY

def purchase_start_view(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed()
    
    if not request.user.is_authenticated:
        return HttpResponseBadRequest()
    
    handle = request.POST.get("handle")

    product = get_object_or_404(Product, handle=handle)

    stripe_price_id = product.stripe_price_id

    if stripe_price_id is None:
        return HttpResponseBadRequest()

    
    success_url = f"{SITE_URL}{reverse('purchase_success')}"
    cancel_url = f"{SITE_URL}{reverse('purchase_stopped')}"

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url
    )

    purchase = Purchase.objects.create(
        user=request.user,
        product=product,
        stripe_price=int(product.price * 100)
    )

    request.session["purchase_id"] = purchase.id

    purchase.stripe_checkout_session_id = checkout_session.id

    purchase.save()

    return HttpResponseRedirect(checkout_session.url)


def purchase_success_view(request: HttpRequest) -> HttpResponse:
    purchase_id = request.session.get("purchase_id")

    purchase = get_object_or_404(Purchase, id=purchase_id)

    purchase.completed = True

    purchase.save()

    del request.session["purchase_id"]

    product = purchase.product

    return redirect("product_detail", product.handle)


def purchase_stopped_view(request: HttpRequest) -> HttpResponse:
    
    purchase_id = request.session.get("purchase_id")
    
    purchase = get_object_or_404(Purchase, id=purchase_id)

    del request.session["purchase_id"]

    product = purchase.product

    return redirect("product_detail", product.handle)