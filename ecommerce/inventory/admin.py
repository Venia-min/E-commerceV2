from django.contrib import admin

from .models import Category, Product, ProductInventory

admin.site.register(Category)
admin.site.register(Product)


class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product", "store_price")


admin.site.register(ProductInventory, InventoryAdmin)
