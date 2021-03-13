import datetime
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.utils import json
from API import serializers
from API.models import Person


@api_view(['POST'])
@csrf_exempt
def loginUser(request):
    try:
        json_data = json.load(request)
        details = json_data["details"]
        serializer = serializers.personSerializer()
        if serializer.check_credentials(details["email"], details["password"]):
            return HttpResponse(json.dumps({"Logged" : True}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"Logged" : False}), content_type='application/json')
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
        serializer = serializers.personSerializer(data=details)
        if serializer.is_valid() and not serializer.email_exists(details["email"]):
            serializer.save()
            return HttpResponse(json.dumps({"signed": True}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"Logged" : False}), content_type='application/json')

    except Exception:
        serializer = serializers.personSerializer()
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)
