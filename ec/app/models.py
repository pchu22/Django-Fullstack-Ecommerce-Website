from django.db import models
import datetime
from django.db.models.signals import post_migrate
from django.dispatch import receiver

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
    
    '''@receiver(post_migrate)
    def create_default_component_types(sender, **kwargs):
        if sender.name == 'app':
            if not component_type.objects.exists():
                component_type.objects.create(
                    type_name='Motherboard', 
                    description='The central printed circuit board (PCB) in many modern computers, which holds many of the crucial components of the system.'
                )
                component_type.objects.create(
                    type_name='CPU', 
                    description='Central Processing Unit, the primary component of a computer that performs most of the processing.'
                )
                component_type.objects.create(
                    type_name='CPU Cooler', 
                    description='A device designed to draw heat away from the system CPU and other components in a computer.'
                )                
                component_type.objects.create(
                    type_name='GPU', 
                    description='Graphics Processing Unit, a specialized electronic circuit designed to accelerate graphics rendering in a computer.'
                )
                component_type.objects.create(
                    type_name='RAM', 
                    description='Random Access Memory, a form of computer memory that is used to store data that is being actively used by a program or operating system.'
                )
                component_type.objects.create(
                    type_name='HDD', 
                    description='A non-volatile storage device that stores and retrieves digital information using magnetic storage. Hard disk drives are commonly used for long-term data storage in computers.'
                )
                component_type.objects.create(
                    type_name='SSD', 
                    description='A data storage device that uses NAND-based flash memory to store data persistently. SSDs are known for their faster read and write speeds compared to traditional HDDs.'
                )
                component_type.objects.create(
                    type_name='PSU', 
                    description='Power Supply Unit, a device that supplies electrical energy to an electrical load.'
                )
                component_type.objects.create(
                    type_name='Optic Drive', 
                    description='A device that uses laser light to read data from or write data to an optical disc.'
                )
                component_type.objects.create(
                    type_name='Sound Card', 
                    description='An expansion card or integrated circuit that provides audio capabilities for a computer.'
                )
                component_type.objects.create(
                    type_name='Wifi Card', 
                    description='A network interface card (NIC) or expansion card that allows a computer to connect to a wireless network. Wifi cards enable wireless communication by transmitting and receiving data using radio waves.'
                )
                component_type.objects.create(
                    type_name='PC Case', 
                    description='The enclosure that contains most of the components of a computer.'
                )
                component_type.objects.create(
                    type_name='Case Fans', 
                    description='Fans installed inside a computer case to provide cooling by dissipating heat.'
                )'''

class supplier(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=30)

    '''@receiver(post_migrate)
    def create_default_component_types(sender, **kwargs):
        if sender.name == 'app':
            if not supplier.objects.exists():
                supplier.objects.create(
                    name='Company1',
                    phone_number='999999999',
                    email='teste@teste.com',
                    address='address1',
                    city='city1',
                    postal_code='1234-123',
                    country='niggaland'
                )'''


    def __str__(self):
        return self.name

class components(models.Model):
    component_id=models.AutoField(primary_key=True)
    component_type = models.ForeignKey(component_type, on_delete=models.CASCADE)
    supplier = models.ForeignKey(supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True, null=True)

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