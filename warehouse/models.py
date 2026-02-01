from django.db import models
from django.conf import settings
from products.models import Product


class Input(models.Model):
    """
    Kirim (Input) model representing stock coming into the warehouse.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Price per Unit", default=0)
    summa = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Total Cost", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.price and self.quantity:
            self.summa = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Input: {self.product.name} - {self.quantity}"
