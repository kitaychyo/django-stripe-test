from django.db import models
import stripe
from django.conf import settings

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[('USD', 'USD'), ('EUR', 'EUR')])

    def __str__(self):
        return self.name

class Discount(models.Model):
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    stripe_coupon_id = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.stripe_coupon_id:
            stripe.api_key = settings.STRIPE_SECRET_KEY_USD  # Используем USD для создания купона
            coupon = stripe.Coupon.create(
                percent_off=self.percentage,
                duration='once',
            )
            self.stripe_coupon_id = coupon.id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.percentage}%"

class Tax(models.Model):
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    stripe_tax_rate_id = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.stripe_tax_rate_id:
            stripe.api_key = settings.STRIPE_SECRET_KEY_USD  # Используем USD для создания налога
            tax_rate = stripe.TaxRate.create(
                display_name='Tax',
                percentage=self.percentage,
                inclusive=False,
            )
            self.stripe_tax_rate_id = tax_rate.id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.percentage}%"

class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)

    def get_total_price(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total -= total * (self.discount.percentage / 100)
        if self.tax:
            total += total * (self.tax.percentage / 100)
        return round(total, 2)

    def get_currency(self):
        return self.items.first().currency if self.items.exists() else 'USD'

    def __str__(self):
        return f"Order {self.id}"