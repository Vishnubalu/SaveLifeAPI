import datetime
import json

from django.core.serializers import serialize
from django.forms import model_to_dict
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.utils import json

from API import serializers


@api_view(['POST'])
@csrf_exempt
def loginUser(request):
    try:
        json_data = json.load(request)
        credentials = json_data["credentials"]
        serializer = serializers.donorSerializer()
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


@api_view(["POST"])
@csrf_exempt
def findDonor_and_Blood(request):
    json_data = json.load(request)
    blood_serializer = serializers.bloodstoreSerializer()
    need = json_data["info"]
    donors = blood_serializer.findBlood(need["bloodType"],
                                     need["state"],
                                     need["district"],
                                     need["mandal"])
    print(type(donors))
    return HttpResponse(json.dumps({"donors": donors}), content_type='application/json')

def getBlood_info(request):
    blood_serializer = serializers.bloodstoreSerializer()
    blood_info = blood_serializer.bloodInfo()
    blood_info_dict = []
    for values in blood_info:
        blood_info_dict.append(values)
    print("after requestS")
    return HttpResponse(json.dumps({"bloodInfo": blood_info_dict}), content_type='application/json')

