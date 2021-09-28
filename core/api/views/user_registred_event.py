from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import EventOrder
from core.api.serializers import EventOrderListSerializer
from core.api.apiviews import MyAPIView

# .................................................................................
# Use rEvent Registered  API
# .................................................................................


class UserEventRegisteredAPIView(MyAPIView):
    
    """
    API View for event listing
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = EventOrderListSerializer

    def get(self, request, format=None):

        """GET method for retrieving the data"""

        if request.user.is_authenticated:

            """ use event id """

            event = EventOrder.objects.filter(user__id=request.user.id)
            serializer = self.serializer_class(event, many=True, context={"request": request})
            return Response({"status": "OK", "message": "Successfully fetched user registered event list", "data": serializer.data})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})