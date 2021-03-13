from typing import List
from django.core.serializers import serialize
from rest_framework import serializers
from django.core.serializers import json
from API.models import Person
from API import models

class personSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields: List[str] = ['name', 'email', 'password', 'phoneNum', 'address', 'bloodType', 'NumDonations', 'NumRequests', 'FundDonations']

    def getPersonDetails(self):
        details = Person.objects.all()
        return serialize('json', details)

    def check_credentials(self, user_email, user_password):
        return Person.objects.filter(email=user_email, password=user_password).exists()

    def email_exists(self, user_email):
        return Person.objects.filter(email=user_email).exists()

