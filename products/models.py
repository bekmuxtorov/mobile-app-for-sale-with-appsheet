from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=255)
    unit = models.ForeignKey(
        Unit, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    # Keeping price as it is fundamental, even if not explicitly in the short list
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    # stock_quantity can be calculated from Inputs - Outputs, but keeping a cached field is good for perf
    stock_quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.unit:
            return f"{self.name} [{self.unit.name}]"
        return self.name
