from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from rest_framework.response import Response


def send_sendgrid_email(context, susbject, recipient_list, template_id):

    message = Mail(from_email=settings.SENDGRID_FROM_EMAIL, to_emails=recipient_list, subject=susbject)
    
    try:
        message.dynamic_template_data = context
        message.template_id = template_id
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
    except Exception as e:
        print(e, "''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''error")
        return Response({"message":e})
