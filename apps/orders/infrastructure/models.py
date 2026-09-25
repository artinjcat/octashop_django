
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class OrderGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_groups")
    address = models.CharField(max_length=255, default='', blank=True)
    phone_number = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='pending')
    
    def __str__(self):
        return f"Order Group {self.id} for {self.user.username}"


class Order(models.Model):
    order_group = models.ForeignKey(OrderGroup, on_delete=models.CASCADE, related_name="orders")
    variant = models.ForeignKey("catalogs.ProductVariant", on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
      return self.variant.product.title
    
    