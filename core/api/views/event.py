from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import Event, UserProfile, InfluencerOffer
from core.api.serializers import EventSerializer, EventListSerializer, InfluencerOfferSerializer
from core.api.apiviews import MyAPIView
from django.utils import timezone

now = timezone.now()

# .................................................................................
# Event API
# .................................................................................


class EventAPIView(MyAPIView):
    
    """
    API View for event listing
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = EventListSerializer

    def get(self, request, format=None):

        """GET method for retrieving the data"""

        if request.user.is_authenticated:

            """ use event id """

            try:
                event = Event.objects.filter(user__id=request.user.id, user__is_influencer=True).order_by('-created_at')
                serializer = self.serializer_class(event, many=True, context={"request": request})
                return Response({"status": "OK", "message": "Successfully fetched event list", "data": serializer.data})

            except Event.DoesNotExist:
                return Response({"status": "FAIL", "message": "Event not found", "data": []})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})



class EventDetailsAPIView(MyAPIView):
    
    """
    API View for event listing
    """

    permission_classes = (AllowAny,)
    serializer_class = EventListSerializer

    def get(self, request, pk,  format=None):

        """GET method for retrieving the data"""

        try:
            event = Event.objects.get(id=pk)
            serializer = self.serializer_class(event, context={"request": request})
            return Response({"status": "OK", "message": "Successfully fetched event details", "data": serializer.data})

        except Event.DoesNotExist:
            return Response({"status": "FAIL", "message": "Event details not found", "data": []})


# Home Page Event List 

class HomePageEventListAPIView(MyAPIView):
    
    """
    API View for event listing
    """

    permission_classes = (AllowAny,)
    serializer_class = EventListSerializer

    def get(self, request, format=None):

        """GET method for retrieving the data"""
        search=request.GET['q']
        if search=='is_featured':
            event = Event.objects.filter(is_featured=True, event_date_time__gte=now, user__is_influencer=True, active=True).order_by('event_date_time')
        elif search=='price':
            event = Event.objects.filter(event_date_time__gte=now, user__is_influencer=True, active=True).order_by("credit_required")
        elif search=='upcoming':
            event = Event.objects.filter(event_date_time__gte=now, user__is_influencer=True, active=True).order_by('event_date_time')
    
        serializer = self.serializer_class(event, many=True, context={"request": request})
        return Response({"status": "OK", "message": "Successfully fetched event list", "data": serializer.data})

    

class UserHomePageEventListAPIView(MyAPIView):
    
    """
    API View for event listing
    """

    permission_classes = (AllowAny,)
    serializer_class = EventListSerializer

    def get(self, request):

        """GET method for retrieving the data"""

        event_result=[]
        search=request.GET['q']
        if search=='all':
            event = Event.objects.filter(event_date_time__gte=now, user__is_influencer=True, active=True).order_by('event_date_time')
            serializer = self.serializer_class(event, many=True, context={"request": request})
            return Response({"status": "OK", "message": "Successfully fetched event list", "data": serializer.data})

        else:
            get_user = UserProfile.objects.filter(influencer__name=search)
            for k in get_user:
                event = Event.objects.filter(user__id=k.user.id, event_date_time__gte=now).order_by('event_date_time')
                serializer = self.serializer_class(event, many=True, context={"request": request})
                for k in serializer.data:
                    event_result.append(k)
            return Response({"status": "OK", "message": "Successfully fetched event list", "data": event_result})


class EventCreateAPI(MyAPIView):

    """API View to create offer"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def post(self, request, format=None):

        """POST method to offer the data"""

        if request.user.is_authenticated:
            request.data._mutable = True
            request.data['user']=request.user.id
            serializer = self.serializer_class(data=request.data,  context={"request": request})
            if serializer.is_valid():
                serializer.save()

                data={
                    'user': request.user.id,
                    "offer": request.data['offer'],
                    'event':serializer.data['id']
                }    

                serializers = InfluencerOfferSerializer(data=data)
                if serializers.is_valid():
                    serializers.save()
               
                return Response({"status": "OK", "message": "Successfully created event", "data": serializer.data})

            else:
                return Response({"status": "FAIL", "message": "Cannot create event", "data": serializer.errors})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class EventUpdateAPI(MyAPIView):

    """API View to update Event Class"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def put(self, request, pk, format=None):

        """ PUT method to offer the data"""

        if request.user.is_authenticated:
            try:
                event = Event.objects.get(pk=pk)
                serializer = self.serializer_class(event, data=request.data, context={"request": request})
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "OK", "message": "Successfully updated  event details.", "data": serializer.data})

                else:
                    return Response({"status": "FAIL", "message": "Cannot update event details", "data": serializer.errors})

            except Event.DoesNotExist:
                return Response({"status": "FAIL", "message": "Event not found", "data": []})
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class EventDeleteAPI(MyAPIView):

    """API View to update Event"""

    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk, format=None):

        """ PUT method to event_class the data"""

        if request.user.is_authenticated:
            try:
                event = Event.objects.get(pk=pk).delete()
                return Response({"status": "OK", "message": "Successfully deleted  event.", "data": []})
            except Event.DoesNotExist:
                return Response({"status": "FAIL", "message": "Event not found", "data": []})
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})
