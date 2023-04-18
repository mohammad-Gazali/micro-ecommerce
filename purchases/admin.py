from django.contrib import admin
from purchases import models



@admin.register(models.Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["id", "timestamp", "product", "display_price", "user"]
    list_select_related = ["product", "user"]
    ordering = ["id"]


    def display_price(self, obj):
        return f"{obj.stripe_price} $"