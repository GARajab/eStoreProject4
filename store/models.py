from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


# customers
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=8)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"(self.first_name){self.last_name}"


# Products
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default="", blank=True, null=True)
    image = models.ImageField(upload_to="uploads/products/")

    def __str__(self):
        return self.name


class Image(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url
