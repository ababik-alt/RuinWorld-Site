from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "preview",
        "name",
        "product_type",
        "price",
        "price_per_unit",
        "featured",
        "active",
        "sort_order",
    )
    list_filter = ("product_type", "featured", "active")
    list_editable = ("featured", "active", "sort_order")
    prepopulated_fields = {"slug": ("name",)}

    def preview(self, obj):
        return format_html(
            '<img src="{}" style="width:56px;height:56px;object-fit:contain;border-radius:12px;background:#111;">',
            obj.display_image,
        )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "player",
        "product",
        "quantity",
        "amount",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("player", "payment_id")
    readonly_fields = (
        "created_at",
        "paid_at",
        "delivered_at",
        "rcon_log",
    )
