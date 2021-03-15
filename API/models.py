import email

from django.db import models
from django.db.models.fields.json import JSONField
# Create your models here.


class Donor(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    fund_donations = models.IntegerField(default=0)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phoneNum = models.CharField(max_length=10)
    address = models.TextField()
    bloodType = models.CharField(max_length=10)
    NumDonations = models.IntegerField(default=0)
    NumRequests = models.IntegerField(default=0)
    FundDonations = models.IntegerField(default=0)


class Bloodstore(models.Model):
    bloodType = models.CharField(max_length=10, default="don't know")
    plasma = models.BooleanField(default=False)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    mandal = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)

    def __str__(self):
        return super(Bloodstore, self).__str__()

class Bloodbanks(models.Model):
    bank_name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    organisedby = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address = models.TextField()
    blood_availability = models.BooleanField(default=False)
    plasma_availability = models.BooleanField(default=False)
    timings = models.TextField(default="24/7")
    details = models.TextField()














