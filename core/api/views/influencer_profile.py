from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.api.apiviews import MyAPIView
from core.api.serializers import (
    InflunecerUserProfileSerializer,
    InflunecerUserProfileUpdateSerializer,
)

from core.models import User, UserProfile

# ........................................................................................
# API For influencer Profile
# ........................................................................................


class InfluencerProfileDetailsView(MyAPIView):
    serializer_class = InflunecerUserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        GET method for retrieving the data
        """
        try:
            user = UserProfile.objects.get(user__id=request.user.id)
            if user is not None:
                serializer = self.serializer_class(user, context={"request": request})
                return Response(
                    {
                        "status": "OK",
                        "message": "Successfully fetched user details",
                        "data": serializer.data,
                    }
                )
        except UserProfile.DoesNotExist:
            return Response({"status": "FAIL", "message": "User not found", "data": []})


class InfluencerProfileUpdateView(MyAPIView):
    serializer_class = InflunecerUserProfileUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        """
        PUT method to update the data
        """
        if request.user.is_authenticated:
            if "name" in request.data.keys():
                User.objects.filter(id=request.user.id).update(
                    name=request.data["name"]
                )
            user_obj = UserProfile.objects.get(user__id=request.user.id)
            serializer = self.serializer_class(
                user_obj, data=request.data, partial=True, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                user_obj = UserProfile.objects.get(user__id=request.user.id)
                new_serializer = InflunecerUserProfileSerializer(
                    user_obj, context={"request": request}
                )
                return Response(
                    {
                        "status": "OK",
                        "message": "Account updated successfully",
                        "data": new_serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "status": "FAIL",
                        "message": "Serializer validation error",
                        "data": serializer.errors,
                    }
                )
        else:
            return Response(
                {"status": "FAIL", "message": "Unauthorised User", "data": []}
            )
