from django.db import models
from django.utils import timezone
import datetime
from enum import Enum
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Create your models here.

class component_type(models.Model):
    component_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50)
    description = models.TextField()
    
    def __str__(self):
        return self.type_name

class warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.address}, {self.postal_code}, {self.city}, {self.country}"

class supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    warehouse = models.ManyToManyField(warehouse)
    
    def __str__(self):
        return self.name

class components(models.Model):
    component_id = models.AutoField(primary_key=True)
    component_type = models.ForeignKey(component_type, on_delete=models.CASCADE)
    supplier = models.ForeignKey(supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class components_purchase(models.Model):
    components_purchase_id = models.AutoField(primary_key=True)
    components = models.ManyToManyField(components)
    timestamps = models.DateTimeField(auto_now_add=True)

class equipment_type(models.Model):
    equipment_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.type_name

class labor_type(models.Model):
    labor_type_id = models.AutoField(primary_key=True)
    labor_name = models.CharField(max_length=30, unique=True)
    #value = models.PositiveIntegerField()

    def __str__(self):
        return self.labor_name
    
class equipments(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    type = models.ForeignKey(equipment_type, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    components = models.ManyToManyField(components)

    def __str__(self):
        return self.name

class production(models.Model):
    production_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    production_start = models.DateTimeField(default=timezone.now)
    production_end = models.DateTimeField()
    labor_type = models.ForeignKey(labor_type, on_delete=models.CASCADE)
    equipment = models.ForeignKey(equipments, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
    
    def save(self, *args, **kwargs):
        if not self.production_date:
            self.production_date = timezone.now()
        super().save(*args, **kwargs)

class users(models.Model):
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12) 
    email = models.EmailField() 
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class orders(models.Model):
    equipments = models.ManyToManyField(equipments, related_name='orders', null=True)
    costumer = models.ForeignKey(users, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    order_date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
