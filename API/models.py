from django.db import models
from django.db.models.fields.json import JSONField
# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phoneNum = models.CharField(max_length=10)
    address = models.TextField()
    bloodType = models.CharField(max_length=10)
    NumDonations = models.IntegerField(default=0)
    NumRequests = models.IntegerField(default=0)
    FundDonations = models.IntegerField(default=0)


    def __str__(self):
        return super().__str__()

class Donations(models.Model):
    person = models.ForeignKey(to=Person, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    donated = models.BooleanField(default=False)
    info = models.JSONField()

    def __str__(self):
        return super().__str__()


class Requests(models.Model):
    person = models.ForeignKey(to=Person, on_delete=models.CASCADE)
    info = models.JSONField()

    def __str__(self):
        return super().__str__()









