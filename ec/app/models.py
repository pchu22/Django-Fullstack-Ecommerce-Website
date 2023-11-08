from django.db import models
import datetime

# Create your models here.

class EquipmentType(models.Model):
    TypeName = models.CharField(max_length=50)
    Description = models.TextField()
    
    def __str__(self):
        return self.TypeName
    
class ComponentType(models.Model):
    TypeName = models.CharField(max_length=50)
    Description = models.TextField()
    
    def __str__(self):
        return self.TypeName

class Supplier(models.Model):
    Name = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=12)
    Email = models.EmailField()
    Address = models.CharField(max_length=50)
    City = models.CharField(max_length=20)
    PostalCode = models.CharField(max_length=10)
    Country = models.CharField(max_length=30)


    def __str__(self):
        return self.Name
    
class Components(models.Model):
    ComponentType = models.ForeignKey(ComponentType, on_delete=models.CASCADE)
    Supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    SerialNumber = models.CharField(max_length=100)
    PurchaseDate = models.DateField()
    PurchasePrice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.Name

class Equipments(models.Model):
    EquipmentType = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)
    Components = models.ManyToManyField(Components, blank=True)
    Name = models.CharField(max_length=50)
    SerialNumber = models.CharField(max_length=100)
    ProductionDate = models.DateField(default=datetime.datetime.today)
    WarrantyExpirationDate = models.DateField()

    def __str__(self):
        return self.Name

class Component_Equipment(models.Model):
    Equipment = models.ForeignKey(Equipments, on_delete=models.CASCADE)
    Component = models.ForeignKey(Components, on_delete=models.CASCADE)
    Quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"The component, {self.Equipment.Name} has {self.Quantity} units of {self.Component.Name}"

class LaborType(models.Model):
    TypeName = models.CharField(max_length=50)
    Description = models.TextField()
    Value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"The labor type {self.TypeName} has the cost of {self.Value}"

class Labor(models.Model):
    Name = models.CharField(max_length=50)
    LaborType = models.ForeignKey(LaborType, on_delete=models.CASCADE)

    def __str__(self):
        return {self.Name}

class Production(models.Model):
    Equipment = models.ForeignKey(Equipments, on_delete=models.CASCADE)
    Components = models.ManyToManyField(Component_Equipment, blank=True)
    Labor = models.ForeignKey(Labor, on_delete=models.CASCADE)
    OrderNumber = models.CharField(max_length=100)
    ProductionDate = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return f"The production of {self.Equipment} will cost {self.Labor.LaborType.Value}€"
    
class Orders(models.Model):
    Equipments = models.ManyToManyField(Equipments, blank=True)
    Costumer = models.ForeignKey(Users, on_delete=models.CASCADE)
    Price = models.DecimalField(max_digits=10, decimal_places=2) 
    OrderDate = models.DateField(default=datetime.datetime.today)
    Status = models.BooleanField(default=False)

    def __str__(self):
        return {self.Name}
