from django.contrib import admin
from products import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "handle", "price", "timestamp", "updated", "user"]
    ordering = ["id"]
    list_select_related = ["user"]


@admin.register(models.ProductAttachment)
class ProductAttachmentAdmin(admin.ModelAdmin):
    pass