from django.db import models
from django.contrib.auth.hashers import make_password
import datetime

# Create your models here.

class equipment_type(models.Model):
    type_name = models.CharField(max_length=50)
    description = models.TextField()
    
    def __str__(self):
        return self.type_name
    
class component_type(models.Model):
    type_name = models.CharField(max_length=50)
    description = models.TextField()
    
    def __str__(self):
        return self.type_name

class supplier(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=30)


    def __str__(self):
        return self.name

class components(models.Model):
    component_type = models.ForeignKey(component_type, on_delete=models.CASCADE)
    supplier = models.ForeignKey(supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class equipments(models.Model):
    type = models.ForeignKey(equipment_type, on_delete=models.CASCADE)
    components = models.ManyToManyField(components, related_name='equipments', null=True)
    name = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, unique=True)
    production_date = models.DateField(default=datetime.datetime.today)
    warranty_expiration_date = models.DateField()

    def __str__(self):
        return self.name

class labor_type(models.Model):
    type_name = models.CharField(max_length=50)
    description = models.TextField()
    value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"The labor type {self.type_name} has the cost of {self.value}"

class labor(models.Model):
    name = models.CharField(max_length=50)
    labor_type = models.ForeignKey(labor_type, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class production(models.Model):
    equipment = models.ForeignKey(equipments, on_delete=models.CASCADE)
    components = models.ManyToManyField(components, related_name='production', null=True)
    labor = models.ForeignKey(labor, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100)
    production_date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return f"The production of {self.equipment} will cost {self.labor.labor_type.value}€"

class profiles(models.Model):
    profile_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.profile_name

class users(models.Model):
    profile = models.ForeignKey(profiles, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12) 
    email = models.EmailField() 
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class orders(models.Model):
    equipments = models.ManyToManyField(equipments, related_name='orders', null=True)
    costumer = models.ForeignKey(users, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    order_date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Costumer {self.costumer.first_name} {self.costumer.last_name} ordered {self.equipments.name} on the day {self.order_date}. Status: {self.status}"