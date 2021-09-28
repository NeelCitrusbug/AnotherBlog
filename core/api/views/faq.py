from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from core.api.pagination import CustomPagination

from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Faq
from core.api.apiviews import MyAPIView
from core.api.serializers import FaqSerializer


# .................................................................................
# Faq Plan API
# .................................................................................


class FaqListAPIView(MyAPIView):

    """
    API View for Faq  listing
    """

    permission_classes = (AllowAny,)
    serializer_class = FaqSerializer

    def get(self, request, format=None):    

        try:
            search=request.GET['q']
            credit = Faq.objects.filter(faq_types=search)
            serializer = self.serializer_class(credit, many=True, context={"request": request})
            return Response({"status": "OK", "message": "Successfully fetched faq list", "data": serializer.data})

        except:
            return Response({"status": "FAIL", "message": "Credit plan not found", "data": []})

