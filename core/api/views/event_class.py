from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import EventClass
from core.api.serializers import EventClassSerializer
from core.api.apiviews import MyAPIView

# .................................................................................
# Event Class API
# .................................................................................


class EventClassAPIView(MyAPIView):
    
    """
    API View for Event Class
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = EventClassSerializer

    def get(self, request, format=None):

        """GET method for retrieving the data"""

        if request.user.is_authenticated:

            """ use event list id """

            event = EventClass.objects.filter(user__id=request.user.id)
            serializer = self.serializer_class(event, many=True, context={"request": request})
            return Response({"status": "OK", "message": "Successfully fetched event class list", "data": serializer.data})
    
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class EventClassCreateAPI(MyAPIView):

    """API View to create Event Class"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EventClassSerializer

    def post(self, request, format=None):

        """POST method to offer the data"""

        if request.user.is_authenticated:
            request.data._mutable = True
            request.data['user']=request.user.id
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "OK", "message": "Successfully created  event class.", "data": serializer.data})

            else:
                return Response({"status": "FAIL", "message": "Cannot create event class", "data": serializer.errors})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class EventClassUpdateAPI(MyAPIView):

    """API View to update Event Class"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EventClassSerializer

    def put(self, request, pk, format=None):

        """ PUT method to offer the data"""

        if request.user.is_authenticated:
            try:
                event_class = EventClass.objects.get(pk=pk)
                serializer = self.serializer_class(event_class, data=request.data, context={"request": request})
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "OK", "message": "Successfully updated  event class.", "data": serializer.data})

                else:
                    return Response({"status": "FAIL", "message": "Cannot update event class", "data": serializer.errors})

            except EventClass.DoesNotExist:
                return Response({"status": "FAIL", "message": "event class not found", "data": []})
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class EventClassDeleteAPI(MyAPIView):

    """API View to update Event Class"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EventClassSerializer

    def delete(self, request, pk, format=None):

        """ PUT method to event_class the data"""

        if request.user.is_authenticated:
            try:
                event_class = EventClass.objects.get(pk=pk).delete()
                return Response({"status": "OK", "message": "Successfully deleted  event class.", "data": []})
            except EventClass.DoesNotExist:
                return Response({"status": "FAIL", "message": "event class not found", "data": []})
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})
