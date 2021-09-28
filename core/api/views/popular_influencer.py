from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import UserProfile
from core.api.apiviews import MyAPIView
from core.api.serializers import InfluencerListSerializer


# .................................................................................
# popular influencer list API
# .................................................................................


class InfluencerListAPIView(MyAPIView):

    """
    API View for popular influencer list  listing
    """

    permission_classes = (AllowAny,)
    serializer_class = InfluencerListSerializer

    def get(self, request, format=None):    
        popular = UserProfile.objects.filter(user__is_influencer=True, is_popular=True).order_by('-created_at')
        serializer = self.serializer_class(popular, many=True, context={"request": request})
        return Response({"status": "OK", "message": "Successfully fetched popular influencer list", "data": serializer.data})


    