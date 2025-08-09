from django.contrib import admin
from .models import Item, Order

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency')
    list_filter = ('currency',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_items_list', 'get_total_price', 'get_currency', 'discount', 'tax')
    list_filter = ('discount', 'tax')
    search_fields = ('id',)
    filter_horizontal = ('items',)

    def get_items_list(self, obj):
        return ", ".join(item.name for item in obj.items.all())
    get_items_list.short_description = 'Items'

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

    def get_currency(self, obj):
        return obj.get_currency()
    get_currency.short_description = 'Currency'