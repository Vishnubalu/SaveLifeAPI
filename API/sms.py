import os
from twilio.rest import Client

def send_sms(sms, number):
    try:
        print("inside send sms")
        account_sid = 'your SID'
        auth_token = 'your TOKEN'
        client = Client(account_sid, auth_token)
        print("after auth")
        numb = "+91" + str(number)
        print(sms)
        message = client.messages \
            .create(
            body=str(sms),
            from_='+18134374746',
            to=numb
        )
        print("after create")
        print(message.status)
    except:
        return "nothing"
