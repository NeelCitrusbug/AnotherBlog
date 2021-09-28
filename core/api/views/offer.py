from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from core.api.pagination import CustomPagination

from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Card, User, InfluencerOffer, Offer
from core.api.serializers import InfluencerOfferSerializer, InfluencerOfferListSerializer, OfferSerializer
from core.api.apiviews import MyAPIView
from core.utils import MyStripe, create_card_object

# .................................................................................
# InfluencerOffer Card API
# .................................................................................


class InfluencerOfferAPIView(MyAPIView):
    
    """
    API View for Card listing
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = OfferSerializer

    def get(self, request, format=None):

        """GET method for retrieving the data"""

        if request.user.is_authenticated:

            """ use offer id """

            try:
                offer = Offer.objects.all()

                serializer = OfferSerializer(offer, many=True, context={"request": request})
                return Response({"status": "OK", "message": "Successfully fetched offer list", "data": serializer.data})

            except Offer.DoesNotExist:
                return Response({"status": "FAIL", "message": "offer not found", "data": []})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class InfluencerOfferCreateAPI(MyAPIView):

    """API View to create offer"""

    permission_classes = (IsAuthenticated,)
    serializer_class = InfluencerOfferSerializer

    def post(self, request, format=None):

        """POST method to offer the data"""

        if request.user.is_authenticated:

                data={
                    'user': request.user.id,
                    "offer": request.data['offer']
                }    
                serializer = InfluencerOfferSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "OK", "message": "Successfully added offer details", "data": serializer.data})

                else:
                    return Response({"status": "FAIL", "message": "Cannot add offer", "data": serializer.errors})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


