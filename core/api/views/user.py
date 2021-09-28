from core.api.permissions import IsSuperUser
from core.api.viewsets import MyModelViewSet
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView

from core.api.serializers import UserSerializer, MyUserSerializer

from rest_framework.permissions import AllowAny

import random
from twilio.rest import Client

from django.utils import timezone
from datetime import datetime, timedelta, date
from core.api.apiviews import MyAPIView


account_sid = 'ACbd44dd22794ad8e0268615ea28eca6fa'
auth_token = 'd4e874adeace90e6cecdc46fb3ca450c'
twilio = '+15005550006'

User = get_user_model()

class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# -----------------------------------------------------------------------------
# My forked version
# -----------------------------------------------------------------------------


class MyUserViewSet(MyModelViewSet):
    
    """
    list:
    List all User

    create:
    Create a User

    retrieve:
    Get a User

    update:
    Update a User

    delete:
    Delete a User
    """

    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (IsSuperUser,)

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return MySerializer



def send_otp(name, recv):        
    my = recv    
    name = name
    client = Client(account_sid, auth_token)
    otp = random.randint(111111, 999999)    
    my_msg = "Hi " + name + " !" + "\n" + "Your Kuzo class account verification otp is : " + str(otp)
    message = client.messages.create(body=my_msg, from_=twilio, to=my)  
    return otp




class AccountCreateApiView(MyAPIView):

    """
    User register view
    """
    serializer_class = MyUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data= request.data
        email = data['email']
        username = data['username']
        mobile_num = data['mobile']
        user = User.objects.filter(email=email).distinct()
        mobile = User.objects.filter(mobile=mobile_num).distinct()

        if user.exists() and mobile.exists():
            return Response({"status": "FAIL", "message": "Account is already exists", "data": []})
#                "data": [],
#                "status": False,
#                "code" : status.HTTP_200_OK,
#                "message" : "Account is already exists."
#                }, status=status.HTTP_200_OK)
        serializer = UserSerializer(data= data)

        if serializer.is_valid(raise_exception = True):
            try:
                
                otp=send_otp(username, mobile_num)
                serializer.save()  
            except:
                return Response({"status": "FAIL", "message": "Cannot sent otp", "data": []})
#                    "status": False,
#                    "code" : status.HTTP_400_BAD_REQUEST,
#                    "message" : "Cannot sent otp"
#                }, status=status.HTTP_400_BAD_REQUEST)

            User.objects.filter(email=email).update(otp=otp)                
          
            return Response({"status": "OK", "message": "Successfully registered User", "data": serializer.data})
#                            "data": serializer.data,
#                            "status": True,
#                            "code" : status.HTTP_200_OK,
#                            "message" : "Successfully registered User"
#                            }, status=status.HTTP_201_CREATED)
        return Response({"status": "FAIL", "message": "Cannot register new user", "data": serializer.errors})
#                        "data": serializer.errors,
#                        "status": False,
#                        "code" : status.HTTP_200_OK,
#                        "message" : "Cannot register new user"
#                        }, status=status.HTTP_200_OK)
        
        
        
class UserOtpVerificationAPIView(MyAPIView):
    permission_classes = (AllowAny,)
    def post(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
            sent_time = user.sent_time + timedelta(seconds=60)
            sent_time = sent_time.astimezone(timezone.utc).replace(tzinfo=None)
           
            if request.data['otp'] == '' or 'otp' not in request.data:
               
                return Response({"status": "FAIL", "message": "OTP is required", "data": []})
#                    "status": False,
#                    "code" : status.HTTP_400_BAD_REQUEST,
#                    "message" : "OTP is required"
#                    }, status=status.HTTP_400_BAD_REQUEST)
            
                                
            else:
                if int(request.data['otp']) == user.otp:
                    user.sms_verification = True
                    user.save()
                    
                    return Response({"status": "OK", "message": "User verified successfully", "data": []})
#                        "status": False,
#                        "code" : status.HTTP_200_OK,
#                        "message" : "User verified successfully"
#                        }, status=status.HTTP_200_OK)
            
            
                else:
                    
                    return Response({"status": "FAIL", "message": "OTP is not match", "data": []})
#                        "status": False,
#                        "code" : status.HTTP_404_NOT_FOUND,
#                        "message" : "OTP is not match."
#                        }, status=status.HTTP_404_NOT_FOUND)
              
        except:
                        
            return Response({"status": "FAIL", "message": "Cannot verify otp", "data": []})
#                "status": False,
#                "code" : status.HTTP_400_BAD_REQUEST,
#                "message" : "Cannot varify otp"
#                }, status=status.HTTP_400_BAD_REQUEST)
