import base64
import datetime

import pyotp
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from API.models import Donor

EXPIRY_TIME = 50 # seconds

class generateKey:
    @staticmethod
    def returnValue(phone):
        print("inside return value")
        print(str(phone) + "Some Random Secret Key")
        return str(phone) + "Some Random Secret Key"

class getPhoneNumberRegistered_TimeBased():
    # Get to Create a call for OTP
    @staticmethod
    def get(phone):
        print("inside get")
        try:
            print("inside try")
            Mobile = Donor.objects.get(phoneNum=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            print("inside except")
            Donor.objects.create(
                phoneNum=phone,
            )
        print("outside try and except")
        Mobile = Donor.objects.get(phoneNum=phone)  # user Newly created Model
        print("after getting mobile")
        Mobile.save()  # Save the data
        print("after saving")
        keygen = generateKey()
        print("after calling generatekey")

        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        print("after key")
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model for OTP is created

        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        return OTP.now()  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(otp, phone):
        print("inside post")
        try:
            print("in try 1")
            Mobile = Donor.objects.get(phoneNum=phone)
            print("in try 2")
        except ObjectDoesNotExist:
            return ("User does not exist")  # False Call
        print("before key gen in post")
        keygen = generateKey()
        try:
            key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        except Exception:
            print(Exception)
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model
        if OTP.verify(otp):  # Verifying the OTP
            return ("You are authorised")
        return ("OTP is wrong/expired")

