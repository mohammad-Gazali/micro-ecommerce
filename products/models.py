from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL
from django.core.validators import MinValueValidator
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
from core.env import config
from core.storages.backends import ProtectedFileStorage
import pathlib
import stripe



STRIPE_PUBLIC_KEY = config("STRIPE_PUBLIC_KEY", default=None)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)

# PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = ProtectedFileStorage()
# protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))


class Product(models.Model):
    name = models.CharField(max_length=127)
    handle = models.SlugField(unique=True)
    image = models.ImageField(upload_to="products/", null=True)
    stripe_product_id = models.CharField(max_length=127, null=True, blank=True)
    stripe_price_id = models.CharField(max_length=127, null=True, blank=True)
    price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    @property
    def stripe_price(self) -> int:
        return int(self.price * 100)
    

    def save(self, *args, **kwargs) -> None:
        
        if self.name:
            stripe_product_response = stripe.Product.create(name=self.name)
            self.stripe_product_id = stripe_product_response.id

        if self.stripe_product_id:
            stripe_price_response = stripe.Price.create(
                product=self.stripe_product_id,
                unit_amount=self.stripe_price,
                currency="usd"
            )
            self.stripe_price_id = stripe_price_response.id
            
        return super().save(*args, **kwargs)
    

def handle_product_attachment_upload(instance, filename: str):
    return f"products/{instance.product.handle}/attachments/{filename}"

class ProductAttachment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.FileField(upload_to=handle_product_attachment_upload, storage=protected_storage)
    name = models.CharField(max_length=127, null=True, blank=True)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # override save method
    def save(self, *args, **kwargs) -> None:
        if not self.name:
            self.name = pathlib.Path(self.file.name).name
        super().save(*args, **kwargs)

    
    @property
    def display_name(self):
        return self.name or pathlib.Path(self.file.name).name