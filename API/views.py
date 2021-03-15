import datetime
import json
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.utils import json
from API import serializers



@api_view(['POST'])
@csrf_exempt
def loginUser(request):
    try:
        json_data = json.load(request)
        details = json_data["details"]
        serializer = serializers.donorSerializer()
        if serializer.check_credentials(details["email"], details["password"]):
            request.session["username"] = details["email"]
            print(request.session.has_key('username'))
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

    json_data = json.load(request)
    details = json_data["details"]

    serializer = serializers.donorSerializer(data = details)

    print(serializer.getDonor())
    print(details)
    print("before if")
    print(serializer.get_validators())
    print(serializer.run_validation(details))
    if serializer.is_valid():
        serializer.save()
        return HttpResponse(json.dumps({"signed": True}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({"signed" : False}), content_type='application/json')



@api_view(['POST'])
@csrf_exempt
def check_session(request):
    s = SessionStore()
    print(s.create())
    print(s.session_key)
    print(request.session.get("username", "vishnu"))
    return HttpResponse(json.dumps({"username": serializers.sessionSerializer().get_session()}), content_type='application/json')



