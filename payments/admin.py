from django.contrib import admin
from .models import Item, Order, OrderItem

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency')
    list_filter = ('currency',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Количество пустых строк для добавления новых OrderItem
    fields = ('item', 'quantity')  # Поля для отображения
    readonly_fields = ()  # Если нужно сделать какие-то поля только для чтения
    can_delete = True  # Разрешить удаление OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_items_list', 'get_total_price', 'get_currency', 'discount', 'tax')
    list_filter = ('discount', 'tax')
    search_fields = ('id',)
    inlines = [OrderItemInline]  # Добавляем Inline для OrderItem

    def get_items_list(self, obj):
        return ", ".join(f"{item.quantity} x {item.item.name}" for item in obj.order_items.all())
    get_items_list.short_description = 'Items'

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

    def get_currency(self, obj):
        return obj.get_currency()
    get_currency.short_description = 'Currency'