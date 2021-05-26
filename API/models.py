from datetime import datetime

from django.db import models


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
    verified = models.IntegerField(default = False)


class Bloodstore(models.Model):
    bloodType = models.CharField(max_length=10, default="don't know")
    plasma = models.BooleanField(default=False)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    mandal = models.CharField(max_length=100)
    area = models.CharField(max_length=100, default=" ")
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

    def __str__(self):
        return super(Bloodbanks, self).__str__()


class Patient(models.Model):
    patient_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField(default="None")
    blood = models.CharField(max_length=10)
    date_need = models.CharField(max_length=10)
    hospital = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=15)
    date_posted = models.CharField(max_length=15, default=datetime.today().strftime('%Y-%m-%d'))
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    mandal = models.CharField(max_length=100)
    message = models.TextField(max_length=1000, default="")

    def __str__(self):
        return super(Patient, self).__str__()


class RequestBlood(models.Model):
    From = models.CharField(max_length=100)
    To = models.CharField(max_length=100)
    Patient = models.CharField(max_length=100, default="")
    Hospital = models.CharField(max_length=100, default="")
    Messege = models.CharField(max_length=1000, default="")
    date_posted = models.CharField(max_length=15, default=datetime.today().strftime('%Y-%m-%d'))

    def __str__(self):
        return super(RequestBlood, self).__str__()