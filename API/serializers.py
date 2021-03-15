from typing import List
from django.contrib.sessions.models import Session
from django.core.serializers import serialize
from rest_framework import serializers
from django.core.serializers import json
from API import models
from API.models import Donor, Bloodstore

class personSerializer(serializers.ModelSerializer):

    # class Meta:
    #     model = Person
    #     fields: List[str] = ['name', 'email', 'password', 'phoneNum', 'address', 'bloodType', 'NumDonations', 'NumRequests', 'FundDonations']
    #
    # def getPersonDetails(self):
    #     details = Person.objects.all()
    #     return serialize('json', details)
    #
    # def check_credentials(self, user_email, user_password):
    #     return Person.objects.filter(email=user_email, password=user_password).exists()
    #
    # def email_exists(self, user_email):
    #     return Person.objects.filter(email=user_email).exists()
    pass

class donorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'

    def getDonor(self):
        details = Donor.objects.all()
        return serialize('json', details)

    def check_credentials(self, donor_email, donor_pass):
        return Donor.objects.filter(email=donor_email, password=donor_pass)

    def donor_exists(self, user_email, user_phone):
        print("inside ", user_email, user_phone)
        return Donor.objects.filter(email=user_email) or Donor.objects.filter(phoneNum=user_phone)


class bloodstoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloodstore
        fields = ['donor', 'bloodType', 'plasma', 'state', 'district', 'mandal', 'area']

class sessionSerializer(serializers.Serializer):
    def get_session(self):
        s = Session.objects.all()
        for session in s:
            print(session.get_decoded())

        return "hehe"


