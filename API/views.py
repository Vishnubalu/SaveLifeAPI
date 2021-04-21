import datetime
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.utils import json
from API import serializers
from API.verification import getPhoneNumberRegistered_TimeBased


@api_view(['POST'])
@csrf_exempt
def loginUser(request):
    try:
        json_data = json.load(request)
        credentials = json_data["credentials"]
        serializer = serializers.donorSerializer()
        print((credentials["check"]))
        if(credentials["check"]):
            print("inside if")
            print(getPhoneNumberRegistered_TimeBased.post(credentials["otp"], credentials["phoneNum"]))

        else:
            print("after if")
            print(getPhoneNumberRegistered_TimeBased.get(credentials["phoneNum"]))
        print("after calls")
        if serializer.check_credentials(credentials["phoneNum"], credentials["password"]):
            return HttpResponse(json.dumps({"Logged": True}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"Logged": False}), content_type='application/json')
    except:
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)


@api_view(['POST'])
@csrf_exempt
def signupUser(request):
    try:
        json_data = json.load(request)
        details = json_data["details"]
        donor_serializer = serializers.donorSerializer(data=details)
        print("before blood serialiser")
        if donor_serializer.is_valid() and \
                donor_serializer.donor_exists(details['phoneNum']):
            donor_serializer.save()
            details["donor"] = donor_serializer.data['id']
            blood_serializer = serializers.bloodstoreSerializer(data=details)
            print(blood_serializer.run_validation(details))
            if blood_serializer.is_valid(details):
                blood_serializer.save()
            return HttpResponse(json.dumps({"signed": True}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"signed": False}), content_type='application/json')
    except:
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)


@api_view(["POST"])
@csrf_exempt
def get_BloodAndDonor_byArea(request):
    try:
        json_data = json.load(request)
        blood_serializer = serializers.bloodstoreSerializer()
        need = json_data["details"]
        donors = blood_serializer.findBlood(need["bloodType"],
                                            need["state"],
                                            need["district"],
                                            need["mandal"])
        return HttpResponse(json.dumps({"donors": donors}), content_type='application/json')
    except:
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)


def getBlood_info(request):
    try:
        blood_serializer = serializers.bloodstoreSerializer()
        blood_info = blood_serializer.bloodInfo()
        blood_info_dict = []
        for values in blood_info:
            blood_info_dict.append(values)
        print("after requestS")
        return HttpResponse(json.dumps({"bloodInfo": blood_info_dict}), content_type='application/json')
    except:
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)


@api_view(['POST'])
@csrf_exempt
def add_bloodbank(request):
    try:
        json_data = json.load(request)
        bloodbank_details = json_data["details"]
        bank_serializer = serializers.bloodbankSerializer(data=bloodbank_details)
        print(bank_serializer.run_validation(bloodbank_details))
        if bank_serializer.is_valid():
            bank_serializer.save()
        return HttpResponse(json.dumps({"signed": True}), content_type='application/json')
    except:
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)


@api_view(["POST"])
@csrf_exempt
def get_bloodbank(request):
    try:
        bank_serializer = serializers.bloodbankSerializer()
        json_data = json.load(request)
        if 'id' in json_data:
            info = bank_serializer.get_bloodBank(json_data['id'])
        else:
            info = bank_serializer.get_bloodBanks(json_data["details"])
        return HttpResponse(json.dumps({"banks": info}), content_type="application/json")
    except:
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)


def add_patient(request):
    try:
        json_data = json.load(request)


    except:
        pass

