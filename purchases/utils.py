from core.env import config
import stripe



STRIPE_PUBLIC_KEY = config("STRIPE_PUBLIC_KEY", default=None)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
SITE_URL = config("SITE_URL", default=None)

stripe.api_key = STRIPE_SECRET_KEY


def product_sales_pipeline(product_name: str, product_price: int):
    stripe_product = stripe.Product.create(name=product_name)

    stripe_product_id = stripe_product.id

    stripe_price = stripe.Price.create(
        product=stripe_product_id,
        unit_amount=product_price,
        currency="usd"
    )

    stripe_price_id = stripe_price.id

    success_url = f"{SITE_URL}/puchases/success"
    cancel_url = f"{SITE_URL}/puchases/stopped"

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

    return checkout_session.url