from django.db import models
from django.conf import settings
from users.models import Customer
from products.models import Product


class Output(models.Model):
    """
    Chiqim (Output) model representing stock going out (Sales).
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Selling Price", default=0)
    summa = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Total Price", blank=True, null=True)
    is_payment = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.price and self.quantity:
            self.summa = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Output: {self.product.name} - {self.quantity} to {self.customer.full_name}"
