
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import random
import string


def validate_ten_digits(value):
    if not value.isdigit() or len(value) != 10:
        raise ValidationError('Number must be exactly 10 digits.')


class CourierShops(models.Model):
    id = models.AutoField(primary_key=True)
    shop_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[validate_ten_digits]
    )
    mobile_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[validate_ten_digits]
    )
    email = models.EmailField(max_length=254, unique=True, blank=True)
    address = models.TextField()
    city = models.TextField()
    state = models.TextField()
    pincode = models.CharField(max_length=10)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.shop_name


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10, validators=[validate_ten_digits])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.customer_name


class Delivery(models.Model):
    id = models.AutoField(primary_key=True)
    courier_shop = models.ForeignKey(CourierShops, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    delivery_address = models.TextField()
    pincode = models.CharField(max_length=10,null=True, blank=True)
    mobile_number = models.CharField(max_length=10, unique=True, validators=[validate_ten_digits])
    delivery_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('In Progress','In Progress'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ])
    tracking_number = models.CharField(max_length=100, unique=True, blank=True)

    class Meta:
        db_table = 'my_app_delivery'
        ordering = ['-delivery_date']
        indexes = [
            models.Index(fields=['tracking_number']),
            models.Index(fields=['delivery_date', 'status'])
        ]
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'

    def __str__(self):
        return f"Delivery {self.tracking_number} to {self.customer_name}"

    def generate_tracking_number(self):
        letters = string.ascii_uppercase
        digits = string.digits
        random_letters = ''.join(random.choice(letters) for _ in range(5))
        random_digits = ''.join(random.choice(digits) for _ in range(4))
        return f"{random_letters}-{random_digits}"

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = self.generate_tracking_number()
        super().save(*args, **kwargs)






































































































# from django.db import models
# from django.core.exceptions import ValidationError
# from django.utils import timezone
# import random
# import string


# def validate_ten_digits(value):
#     if len(str(value)) != 10:
#         raise ValidationError('Number must be exactly 10 digits.')

# class CourierShops(models.Model):
#     id = models.AutoField(primary_key=True)
#     shop_name = models.CharField(max_length=100)
#     owner_name = models.CharField(max_length=100)
#     phone_number = models.BigIntegerField(
#         unique=True,
#         validators=[validate_ten_digits])
#     mobile_number = models.BigIntegerField(
#         unique=True,
#         validators=[validate_ten_digits])
#     email = models.EmailField(max_length=254, unique=True, blank=True)
#     address = models.TextField()
#     city = models.TextField()
#     state = models.TextField()
#     pincode = models.CharField(max_length=10, null=True, blank=True)
#     status = models.BooleanField(default=True)

#     def __str__(self):
#         return self.shop_name
    
# class Customer(models.Model):
#     id = models.AutoField(primary_key=True)
#     customer_name = models.CharField(max_length=255) 
#     billing_address = models.CharField(max_length=255)
#     pincode = models.CharField(max_length=10, null=True, blank=True)
#     phone_number = models.CharField(max_length=15)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     status = models.CharField(max_length=50)
     
#     def __str__(self):
#         return self.customer_name

# class Delivery(models.Model):
#     id = models.AutoField(primary_key=True)
#     courier_shop = models.ForeignKey(CourierShops, on_delete=models.CASCADE)
#     customer_name = models.CharField(max_length=255) 
#     delivery_address = models.TextField()
#     pincode = models.CharField(max_length=10, null=True, blank=True)
#     mobile_number = models.CharField(max_length=10, unique=True) 
#     delivery_date = models.DateTimeField(default=timezone.now)
#     status = models.CharField(max_length=50, choices=[
#         ('Pending', 'Pending'),
#         ('In Progress', 'In Progress'),
#         ('Delivered', 'Delivered'),
#         ('Cancelled', 'Cancelled')
#     ])
#     tracking_number = models.CharField(max_length=100, unique=True, blank=True)

#     class Meta:
#         db_table = 'delivery'
#         ordering = ['-delivery_date']
#         indexes = [
#             models.Index(fields=['tracking_number']),
#             models.Index(fields=['delivery_date', 'status'])
#         ]
#         verbose_name = 'Delivery'
#         verbose_name_plural = 'Deliveries'

#     def __str__(self):
#         return f"Delivery {self.tracking_number} to {self.customer_name}"

#     def generate_tracking_number(self):
#         letters = string.ascii_uppercase
#         digits = string.digits
#         random_letters = ''.join(random.choice(letters) for _ in range(5))
#         random_digits = ''.join(random.choice(digits) for _ in range(4))
#         return f"{random_letters}-{random_digits}"

#     def save(self, *args, **kwargs):
#         if not self.tracking_number:
#             self.tracking_number = self.generate_tracking_number()
#         super().save(*args, **kwargs)
