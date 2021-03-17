from django.contrib.sessions.models import Session
from django.core.serializers import serialize
from django.db.models import Count
from rest_framework import serializers

from API.models import Donor, Bloodstore


class donorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'

    def getDonor(self, user_ids):
        details = Donor.objects.all()
        donors = details.filter(id__in=user_ids)
        return donors.values()

    def check_credentials(self, donor_phone, donor_pass):
        return Donor.objects.filter(phoneNum=donor_phone, password=donor_pass).exists()

    def donor_exists(self, user_phone):
        return (not Donor.objects.filter(phoneNum=user_phone).exists())


class bloodstoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloodstore
        fields = '__all__'

    def getBlood(self, user_ids):
        blood = Bloodstore.objects.all()
        return serialize('json', blood)

    def findBlood(self, need_bloodType, need_state, need_district, need_mandal):
        blood = Bloodstore.objects.all()
        blood = blood.filter(bloodType=need_bloodType,
                           state=need_state,
                           district=need_district,
                           mandal=need_mandal).values()
        donors = blood.values_list("donor_id", flat=True)
        donors = donorSerializer().getDonor(user_ids=donors)
        donors_list = []
        for i in range(len(donors)):
            donors[i].update(blood[i])
            donors[i].pop("password")
            donors[i].pop("id")
            donors[i].pop("donor_id")
            donors_list.append(donors[i])
        return donors_list

    def bloodInfo(self):
        blood_info = Bloodstore.objects.values("bloodType").annotate(Count("bloodType"))
        return blood_info

