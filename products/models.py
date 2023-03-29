from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL
from django.core.validators import MinValueValidator



class Product(models.Model):
    name = models.CharField(max_length=127)
    handle = models.SlugField(unique=True)
    image = models.ImageField(upload_to="products/", null=True)
    price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=10, decimal_places=2, default=0) # type: ignore
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    @property
    def stripe_price(self) -> int:
        return int(self.price * 100)