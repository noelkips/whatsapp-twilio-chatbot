from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.CharField(null=True, blank=True, max_length=100)
    phodeId = models.CharField(null=True, blank=True, max_length=200)

    uniqueId = models.CharField(null=True, blank=True, unique=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created=timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.last_updated = timezone.localtime(timezone.now())
        super(Profile, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100)

    uniqueId = models.CharField(null=True, blank=True, unique=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created=timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.last_updated = timezone.localtime(timezone.now())
        super(Category, self).save(*args, **kwargs)


    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    uniqueId = models.CharField(null=True, blank=True, unique=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created=timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.last_updated = timezone.localtime(timezone.now())
        super(Product, self).save(*args, **kwargs)


    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    amount =  models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    uniqueId = models.CharField(null=True, blank=True, unique=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    
    def amount(self, *args, **kwargs):
        quantitiy =self.quantity
        price = self.product.price
        return quantitiy *price 
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created=timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.last_updated = timezone.localtime(timezone.now())
        super(Order, self).save(*args, **kwargs)


    def __str__(self):
        return self.product_name

class ChatSession(models.Model):
    selected_category = models.IntegerField(null=True, blank=True)
    selected_product = models.IntegerField(null=True, blank=True)
    ordered_product = models.IntegerField(null=True, blank=True)
    is_order_successful = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


    uniqueId = models.CharField(null=True, blank=True, unique=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created=timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.last_updated = timezone.localtime(timezone.now())
        super(ChatSession, self).save(*args, **kwargs)

