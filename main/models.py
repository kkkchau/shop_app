from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.name

class Service(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='created')
    full_name = models.CharField(max_length=255, blank=False, default='')
    phone_number = models.CharField(max_length=20, blank=False, default='')
    address = models.CharField(max_length=255, blank=False, default='')
    email = models.EmailField(blank=False, default='')

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    
    def get_total_cost(self):
        total_cost = sum(item.product.price * item.quantity for item in self.orderitem_set.all())
        return total_cost

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name if self.product else self.service.name} in order {self.order.id}'

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
