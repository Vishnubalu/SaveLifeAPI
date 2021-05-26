from datetime import datetime

from django.core.serializers import serialize
from django.db.models import Count
from rest_framework import serializers

from API.models import Donor, Bloodstore, Bloodbanks, Patient, RequestBlood


class donorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'

    def getTotalRegistred(self):
        registered = Donor.objects.values("phoneNum").count()
        return registered

    def getDonor(self, user_ids):
        details = Donor.objects.all()
        donors = details.filter(id__in=user_ids)
        return donors.values()

    def check_credentials(self, phoneNum, donor_pass):
        return Donor.objects.filter(phoneNum=phoneNum, password=donor_pass).exists()

    def donor_exists(self, phoneNum):
        return (not Donor.objects.filter(phoneNum=phoneNum).exists())

    def donor_info(self, phoneNum):
        return Donor.objects.filter(phoneNum=phoneNum).values()





class bloodstoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloodstore
        fields = '__all__'

    def getBlood(self):
        blood = Bloodstore.objects.all()
        return serialize('json', blood)

    def findBlood(self, need_bloodType, need_state, need_district, need_mandal):
        blood = Bloodstore.objects.all()

        if(need_state=="" and need_bloodType == ""):
            blood = blood.all().order_by("state").values()

        elif(need_state == "" and need_bloodType != ""):
            blood = blood.filter(bloodType=need_bloodType).order_by("state").values()

        elif(need_mandal == ""):
            blood = blood.filter(bloodType=need_bloodType,
                                 state=need_state,
                                 district=need_district).values()
        else:
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


class bloodbankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloodbanks
        fields = "__all__"

    def getTotalbanks(self):
        total_banks = Bloodbanks.objects.values("bank_name").count()
        return total_banks

    def get_bloodBank(self, id):
        banks = Bloodbanks.objects.all()
        banks = banks.filter(id=id).values()
        banks_list = []
        for bank in banks:
            banks_list.append(bank)
        return banks_list

    def get_bloodBanks(self, details):
        print("inside get blood banks")
        banks = Bloodbanks.objects.all()
        print("after banks")
        print(details["state"], details["district"])
        banks = banks.filter(state=details["state"],
                             district=details["district"]).values()
        print("after filter")
        banks_list = []
        for bank in banks:
            banks_list.append(bank)
        return banks_list


class patientSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"

    def getAllPatients(self):
        today = datetime.today().strftime('%Y-%m-%d')
        Patient.objects.filter(date_need__lt = today).delete()
        patients = Patient.objects.all().order_by("date_need").values()
        return patients

class requestSerialiser(serializers.ModelSerializer):
    class Meta:
        model = RequestBlood
        fields = "__all__"

    def getRequests(self, To):
        requests = RequestBlood.objects.filter(To=To).values()
        return requests

