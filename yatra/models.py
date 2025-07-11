from django.db import models
from django import forms
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


# Create your models here.
class Destination(models.Model):
    id = models.IntegerField(primary_key=True)
    place = models.CharField(max_length=20)
    img1 = models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    number = models.IntegerField(default=2)

class Detailed_desc(models.Model):
    dest_id = models.AutoField(primary_key=True)
    place = models.CharField(max_length=20)
    days = models.IntegerField(default=5)
    price = models.IntegerField(default=20000)
    rating = models.IntegerField(default=5)
    dest_name = models.CharField(max_length=25)
    img1=models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    desc = models.TextField()
    day1= models.CharField(max_length=200)
    day2 = models.CharField(max_length=200)
    day3 = models.CharField(max_length=200)
    day4 = models.CharField(max_length=200)
    day5 = models.CharField(max_length=200)
    day6 = models.CharField(max_length=200)

class pessanger_detail(models.Model):
    Trip_id = models.AutoField(primary_key=True)
    Trip_same_id = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    Trip_date = models.DateField()
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Trip ID: {self.Trip_id}"
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#class Payment(models.Model):
 
 #   mobile_number = models.CharField(primary_key=True, max_length=16)
  #  password = models.CharField(max_length=2)
   # Balance = models.CharField(max_length=8)
    #email=models.EmailField(max_length=50,default='rambarodavala21@gmail.com')

class Transactions(models.Model):
    Transactions_ID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10)
    Trip_same_id = models.IntegerField(default=1)
    Amount = models.CharField(max_length=8)
    Status = models.CharField(default="Failed", max_length=15)
    Payment_method = models.CharField(blank=True, max_length=15)
    Date_Time = models.CharField(default=timezone.now(), max_length=19)