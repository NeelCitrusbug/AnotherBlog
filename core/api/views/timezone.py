from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import Banner
from core.api.apiviews import MyAPIView
from core.api.serializers import TimezoneSerializer

from pytz import timezone
import datetime, pytz

# .................................................................................
# banner Plan API
# .................................................................................


class TimezoneListAPIView(MyAPIView):

    """
    API View for banner  listing
    """

    permission_classes = (AllowAny,)
    serializer_class = TimezoneSerializer

    def get(self, request, format=None):    
        get_imezone = pytz.common_timezones
        a=[]
        for k in get_imezone:
            
            timezone_code = datetime.datetime.now(tz=pytz.timezone(k))
            data=timezone_code.strftime("%Z")
            if not any(i==data for i in a) and data.isalpha():
                a.append(data)

        return Response({"status": "OK", "message": "Successfully fetched timezone list", "data": a})


    