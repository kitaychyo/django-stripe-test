from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='usd')

    def __str__(self):
        return f"{self.name} ({self.currency})"

class Discount(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Процент скидки
    stripe_coupon_id = models.CharField(max_length=100, blank=True)  # ID купона в Stripe

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    stripe_tax_rate_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total *= (1 - self.discount.percentage / 100)
        if self.tax:
            total *= (1 + self.tax.percentage / 100)
        return total

    def get_currency(self):
        return self.items.first().currency if self.items.exists() else 'usd'

    def __str__(self):
        return f"Order {self.id}"