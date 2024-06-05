from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, default='/static/images/default_cover.png')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
        ('choosing', 'В корзине'),
        ('pending', 'В ожидании'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='choosing')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    @property
    def total_price(self):
        total_price = 0
        for item in self.items.all():
            total_price += item.item_price
        return total_price


class OrderItem(models.Model):
    cart = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    @property
    def item_price(self):
        return self.product.price * self.quantity
