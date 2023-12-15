from django.db import models
import datetime
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
    image = models.URLField(blank=True, null=True)

class components_purchase(models.Model):
    components_purchase_id = models.AutoField(primary_key=True)
    components = models.ManyToManyField(components)
    timestamps = models.DateTimeField(auto_now_add=True)

class equipment_type(models.Model):
    equipment_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50)
    description = models.TextField()

class equipments(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    type = models.ForeignKey(equipment_type, on_delete=models.CASCADE)
    components = models.ManyToManyField(components, related_name='equipments', null=True)
    name = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, unique=True)
    production_date = models.DateField(default=datetime.datetime.today)
    warranty_expiration_date = models.DateField()

class labor_type(models.Model):
    type_name = models.CharField(max_length=50)
    description = models.TextField()
    value = models.DecimalField(max_digits=5, decimal_places=2)

class labor(models.Model):
    name = models.CharField(max_length=50)
    labor_type = models.ForeignKey(labor_type, on_delete=models.CASCADE)

class production(models.Model):
    equipment = models.ForeignKey(equipments, on_delete=models.CASCADE)
    components = models.ManyToManyField(components, related_name='production', null=True)
    labor = models.ForeignKey(labor, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100)
    production_date = models.DateField(default=datetime.datetime.today)

class profiles(models.Model):
    profile_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

class users(models.Model):
    profile = models.ForeignKey(profiles, on_delete=models.CASCADE)
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
