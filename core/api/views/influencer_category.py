from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import Category
from core.api.apiviews import MyAPIView
from core.api.serializers import InfluencerCategorySerializer


# .................................................................................
# Category API
# .................................................................................


class CategoryListAPIView(MyAPIView):

    """
    API View for Category  listing
    """

    permission_classes = (AllowAny,)
    serializer_class = InfluencerCategorySerializer

    def get(self, request, format=None):    
        category = Category.objects.all()
        serializer = self.serializer_class(category, many=True, context={"request": request})
        return Response({"status": "OK", "message": "Successfully fetched list data", "data": serializer.data})


    