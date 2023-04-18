from django.db import models
from django.conf import settings
from django.conf.global_settings import AUTH_USER_MODEL
from products.models import Product



class Purchase(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    stripe_price = models.IntegerField(default=0)
    stripe_checkout_session_id = models.CharField(max_length=127, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
