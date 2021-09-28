from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import Agenda
from core.api.serializers import EventAgendaSerializer
from core.api.apiviews import MyAPIView

# .................................................................................
# Agenda API
# .................................................................................


class EventAgendaAPIView(MyAPIView):
    
    """
    API View for event agenda listing
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = EventAgendaSerializer

    def get(self, request,pk, format=None):

        """GET method for retrieving the data"""

        if request.user.is_authenticated:

            """ use event id """

            try:
                event_agenda = Agenda.objects.filter(event__id=pk)
                serializer = self.serializer_class(event_agenda, many=True, context={"request": request})
                return Response({"status": "OK", "message": "Successfully fetched event agenda list", "data": serializer.data})

            except Agenda.DoesNotExist:
                return Response({"status": "FAIL", "message": "Event agenda not found", "data": []})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class EventAgendaCreateAPI(MyAPIView):

    """API View to create Agenda"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EventAgendaSerializer

    def post(self, request, format=None):

        """POST method to Event Agenda the data"""

        if request.user.is_authenticated:

            serializer = self.serializer_class(data=request.data,  context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "OK", "message": "Successfully created event agenda", "data": serializer.data})

            else:
                return Response({"status": "FAIL", "message": "Cannot create event agenda", "data": serializer.errors})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class EventAgendaUpdateAPI(MyAPIView):

    """API View to update Event Agenda"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EventAgendaSerializer

    def put(self, request, pk, format=None):

        """ PUT method to agenda the data"""

        if request.user.is_authenticated:
            try:
                event_agenda = Agenda.objects.get(pk=pk)
                serializer = self.serializer_class(event_agenda, data=request.data, context={"request": request})
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "OK", "message": "Successfully updated  event agenda details.", "data": serializer.data})

                else:
                    return Response({"status": "FAIL", "message": "Cannot update event agenda details", "data": serializer.errors})

            except Agenda.DoesNotExist:
                return Response({"status": "FAIL", "message": "Event agenda not found", "data": []})
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class EventAgendaDeleteAPI(MyAPIView):

    """API View to update Event Agenda"""

    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk, format=None):

        """ PUT method to agenda the data"""

        if request.user.is_authenticated:
            try:
                event_agenda = Agenda.objects.get(pk=pk).delete()
                return Response({"status": "OK", "message": "Successfully deleted event agenda.", "data": []})
            except Agenda.DoesNotExist:
                return Response({"status": "FAIL", "message": "Event agenda not found", "data": []})
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})
