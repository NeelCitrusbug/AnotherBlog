from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import EventPracticeAudienceQA
from core.api.serializers import EventPracticeAudienceQASerializer
from core.api.apiviews import MyAPIView

# .................................................................................
# Event Practice Audience QA API
# .................................................................................


class EventPracticeAudienceQAAPIView(MyAPIView):
    
    """
    API View for Event Practice Audience QA  listing
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = EventPracticeAudienceQASerializer

    def get(self, request,pk, format=None):

        """GET method for retrieving the data"""

        if request.user.is_authenticated:

            """ use Event Practice Audience QA  id """

            try:
                event = EventPracticeAudienceQA.objects.filter(event__id=pk)
                serializer = self.serializer_class(event, many=True, context={"request": request})
                return Response({"status": "OK", "message": "Successfully fetched event practice q.a list", "data": serializer.data})

            except EventPracticeAudienceQA.DoesNotExist:
                return Response({"status": "FAIL", "message": "Event Q.A list not found", "data": []})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class EventPracticeAudienceQACreateAPI(MyAPIView):

    """API View to create Event Practice Audience QA """

    permission_classes = (IsAuthenticated,)
    serializer_class = EventPracticeAudienceQASerializer

    def post(self, request, format=None):

        """POST method to Event Practice Audience QA  the data"""

        if request.user.is_authenticated:

            serializer = self.serializer_class(data=request.data,  context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "OK", "message": "Successfully created Event Practice Audience QA.", "data": serializer.data})

            else:
                return Response({"status": "FAIL", "message": "Cannot create Event Practice Audience QA ", "data": serializer.errors})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class EventPracticeAudienceQAUpdateAPI(MyAPIView):

    """API View to update Event Practice Audience QA """

    permission_classes = (IsAuthenticated,)
    serializer_class = EventPracticeAudienceQASerializer

    def put(self, request, pk, format=None):

        """ PUT method to Event Practice Audience QA  the data"""

        if request.user.is_authenticated:
            try:
                event = EventPracticeAudienceQA.objects.get(pk=pk)
                serializer = self.serializer_class(event, data=request.data, context={"request": request})
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "OK", "message": "Successfully updated  event practice audience QA details.", "data": serializer.data})

                else:
                    return Response({"status": "FAIL", "message": "Cannot update event practice audience QA details", "data": serializer.errors})

            except EventPracticeAudienceQA.DoesNotExist:
                return Response({"status": "FAIL", "message": "Event practice audience QA not found", "data": []})
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class EventPracticeAudienceQADeleteAPI(MyAPIView):

    """API View to update event practice audience QA"""

    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk, format=None):

        """ PUT method to event practice audience QA the data"""

        if request.user.is_authenticated:
            try:
                event = EventPracticeAudienceQA.objects.get(pk=pk).delete()
                return Response({"status": "OK", "message": "Successfully deleted  event practice audience QA.", "data": []})
            except EventPracticeAudienceQA.DoesNotExist:
                return Response({"status": "FAIL", "message": "Event practice audience QA not found", "data": []})
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})
