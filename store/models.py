from django.db import models


'''
Relations:

Customer - Order : One - Many
Collection - Product : One - Many
Customer - Address : One - Many
Promotion - Product : Many - Many

'''

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.PositiveSmallIntegerField()


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default=None)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    inventory = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    promotions = models.ManyToManyField(Promotion) 

class Collection(models.Model):
    title = models.CharField(max_length=255)
    product = models.ForeignKey(to=Product, on_delete = models.PROTECT)
    # featured_product= models.ForeignKey(Product)

class Customer(models.Model):
    MEMEBERSHIP_BRONZE = 'B'
    MEMEBERSHIP_SILVER = 'S'
    MEMEBERSHIP_GOLD = 'G'
    
    MEMEBERSHIP_CHOICES = [
        (MEMEBERSHIP_BRONZE, 'Bronze'),
        (MEMEBERSHIP_SILVER, 'Silver'),
        (MEMEBERSHIP_GOLD, 'Gold'),
    ]
     
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, default=None)
    membership = models.CharField(max_length=1, choices=MEMEBERSHIP_CHOICES, default=MEMEBERSHIP_BRONZE)


class Order(models.Model):

    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_COMPLETED = 'C'
    PAYMENT_STATUS_PENDING = 'P'

    PAYMENT_STATUS_CHOIES = [
        (PAYMENT_STATUS_PENDING,'Pending'),
        (PAYMENT_STATUS_FAILED,'Failed'),
        (PAYMENT_STATUS_COMPLETED,'Completed')
    ]

    placed_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=1, default=PAYMENT_STATUS_PENDING, choices=PAYMENT_STATUS_CHOIES)
    customer = models.ForeignKey(to=Customer, on_delete = models.PROTECT)


class Address(models.Model):
    street= models.CharField(max_length=255)
    city= models.CharField(max_length=255)
    customer = models.ForeignKey(to=Customer, on_delete = models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete = models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    product = models.ForeignKey(Product, on_delete = models.PROTECT)
    unit_price= models.DecimalField(max_digits=8, decimal_places=2)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CardItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete = models.DO_NOTHING)
    quantity = models.IntegerField()

