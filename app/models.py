from pyexpat import model


from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator


# Create your models here.

state_choices = (
    ("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),
    ("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),
    ("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),
    ("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),
    ("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),
    ("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),
    ("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),
    ("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),
    ("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),
    ("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),
    ("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),
    ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),
    ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),
    ("National Capital Territory of Delhi","National Capital Territory of Delhi"),
    ("Puducherry","Puducherry"), ("Lakshadweep","Lakshadweep"),)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    locality = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    state = models.CharField(choices=state_choices, max_length=100)

    def __str__(self):
        return str(self.id)
#################################################################################################


category_choices = (
    ('BW', 'Bottom Wear'),
    ('TW', 'Top Wear'),
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('B', 'Book')
)

class Product(models.Model):
    title = models.CharField(max_length=300)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField(max_length=10000)
    brand = models.CharField(max_length=200)
    category = models.CharField(choices=category_choices, max_length=2)
    product_image = models.ImageField(upload_to='producting')

    def __str__(self):
        return str(self.id)
#################################################################################################

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
#################################################################################################

status_choices = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
