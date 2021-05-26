import datetime
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.utils import json
from API import serializers
from API.verification import getPhoneNumberRegistered_TimeBased
from API.sms import send_sms


@api_view(['POST'])
@csrf_exempt
def loginUser(request):
    try:
        json_data = json.load(request)
        credentials = json_data["credentials"]
        serializer = serializers.donorSerializer()
        if serializer.check_credentials(credentials["phoneNum"], credentials["password"]):
            user = serializer.donor_info(credentials["phoneNum"])
            print(user[0])
            if(user[0]["verified"]):
                return HttpResponse(json.dumps({"credentials": True,
                                            "verified" : True,
                                            "user_info" : {"user_name" : user[0]["user_name"], "phoneNum" : user[0]["phoneNum"]}}),
                                content_type='application/json')
            else:
                user = serializer.donor_info(credentials["phoneNum"])
                getPhoneNumberRegistered_TimeBased().get(credentials["phoneNum"])
                return HttpResponse(json.dumps({"credentials": True,
                                                "verified": False,
                                                "user_info" : {"user_name" : user[0]["user_name"], "phoneNum" : user[0]["phoneNum"]}}),
                                    content_type='application/json')
        else:
            return HttpResponse(json.dumps({"credentials": False}), content_type='application/json')
    except:
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)

@api_view(['POST'])
@csrf_exempt
def verify_otp(request):
    try:
        json_data = json.load(request)
        credentials = json_data["details"]
        print(credentials)
        if(getPhoneNumberRegistered_TimeBased().post(credentials["otp"], credentials["phoneNum"])):

            return HttpResponse(json.dumps({
                                    "verified": True}),
                        content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                "verified": False}),
                content_type='application/json')
    except:
        now = datetime.datetime.now()
        print("exception")
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
        print(donor_serializer.is_valid())
        print(donor_serializer.donor_exists(details['phoneNum']))
        if donor_serializer.is_valid() and \
                donor_serializer.donor_exists(details['phoneNum']):
            donor_serializer.save()
            details["donor"] = donor_serializer.data['id']
            blood_serializer = serializers.bloodstoreSerializer(data=details)
            print(blood_serializer.run_validation(details))
            if blood_serializer.is_valid(details):
                print("inside if condition")
                blood_serializer.save()
            return HttpResponse(json.dumps({"signed": True}), content_type='application/json')
        else:
            print("inside else condition")
            return HttpResponse(json.dumps({"signed": False}), content_type='application/json')
    except:
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)


@api_view(["POST"])
@csrf_exempt
def get_BloodAndDonor_byArea(request):
    try:
        print("inside get donors")
        json_data = json.load(request)
        blood_serializer = serializers.bloodstoreSerializer()
        need = json_data["details"]
        donors = blood_serializer.findBlood(need["bloodType"],
                                            need["state"],
                                            need["district"],
                                            need["mandal"])
        print(donors)

        return HttpResponse(json.dumps({"donors": donors}), content_type='application/json')
    except:
        now = datetime.datetime.now()
        print("exception")
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)


def getBlood_info(request):
    try:
        blood = ["A-" ,"A+", "O-", "O+", "AB-", "AB+", "B+", "B-"]
        blood_serializer = serializers.bloodstoreSerializer()
        blood_info = blood_serializer.bloodInfo()
        donor_serializer = serializers.donorSerializer()
        total_registered = donor_serializer.getTotalRegistred()
        bank_serializer = serializers.bloodbankSerializer()
        total_banks = bank_serializer.getTotalbanks()
        print(total_registered, total_banks)
        blood_info_dict = []
        for values in blood_info:
            blood.remove(values["bloodType"])
            blood_info_dict.append(values)

        for value in blood:
            blood_info_dict.append({"bloodType" : value, "bloodType__count" : 0})

        return HttpResponse(json.dumps({"bloodInfo": blood_info_dict,
                                        "total_banks" : total_banks,
                                        "total_donors" : total_registered}), content_type='application/json')
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
            print(json_data)
            info = bank_serializer.get_bloodBanks(json_data["details"])
        print(info)
        return HttpResponse(json.dumps({"donors": info}), content_type="application/json")
    except:
        print("except")
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)

@api_view(["POST"])
@csrf_exempt
def add_patient(request):
    try:
        json_data = json.load(request)

        patient_details = json_data["details"]
        print(patient_details)
        patient_serializer = serializers.patientSerialiser(data=patient_details)
        print(patient_serializer.run_validation(patient_details))
        print(patient_serializer.is_valid());
        if patient_serializer.is_valid():
            print("inside if")
            patient_serializer.save()

        return HttpResponse(json.dumps({"created": True}), content_type='application/json')
    except:
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)

@api_view(["GET"])
@csrf_exempt
def get_patients(request):
    patient_serializer = serializers.patientSerialiser()
    patient_info = patient_serializer.getAllPatients()
    patient_info_dict = []
    for values in patient_info:
        patient_info_dict.append(values)
    print(patient_info_dict)
    return HttpResponse(json.dumps({"patients": patient_info_dict}), content_type='application/json')


@api_view(["POST"])
@csrf_exempt
def SMS(request):
    try:
        json_data = json.load(request)
        sms_details = json_data["details"]
        contact = sms_details["From"]
        name = sms_details["Name"]
        hospital = sms_details["Hospital"]
        messege = sms_details["Messege"]
        to = sms_details["To"]
        #getPhoneNumberRegistered_TimeBased().get(to)
        print(to)
        messege = contact + " " + name
        send_sms(messege, to)
        return HttpResponse(json.dumps({"done": True}), content_type='application/json')
    except:
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)

@api_view(["POST"])
@csrf_exempt
def Make_request(request):
    try:
        json_data = json.load(request)
        details = json_data["details"]
        print(details)
        request_serialiser = serializers.requestSerialiser(data=details)
        print(request_serialiser.run_validation(details))
        print(request_serialiser.is_valid());
        if request_serialiser.is_valid():
            print("inside if")
            request_serialiser.save()
        return HttpResponse(json.dumps({"created": True}), content_type='application/json')
    except:
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)






