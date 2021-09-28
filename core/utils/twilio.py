from twilio.rest import Client
from django.conf import settings
from twilio.base.exceptions import TwilioRestException


def send_sms(phone, text):
    account_sid = settings.ACCOUNT_SID  # os.getenv("ACCOUNT_SID", "ACbfa61a1b125390190d32526bc183b27d")
    auth_token = settings.AUTH_TOKEN  # os.getenv("TWILIO_AUTH_TOKEN", "eb9ea79b7fbcd1022544ac53419bd338")
    from_number = settings.FROM_NUMBER

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to='+91' + phone,
            from_=from_number,  # os.getenv("TWILIO_FORM_NUMBER", "+14192859494"),
            body=text)
        print(message.sid)
        return message
    except TwilioRestException as e:
        print(e)
        return str(e)

    # print('-------------------------------------------SMS------------------------------------------------')
    # print(message)
    # print(text)
    # print('-------------------------------------------SMS------------------------------------------------')
