from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from core.api.apiviews import MyAPIView
from core.api.serializers import UserUpdateDetailsSerializer
from core.api.serializers.rest_auth.login import ProfileDetailsSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.utils import modify_api_response
from core.models import User, UserProfile

# ........................................................................................
# API For Profile
# ........................................................................................


class ProfileDetailsView(MyAPIView):

    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.

    Default accepted fields: username, first_name, last_name
    Default display fields: pk, username, email, first_name, last_name
    Read-only fields: pk, email

    Returns UserModel fields.
    """

    serializer_class = ProfileDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        GET method for retrieving the data
        """

        try:
            user = UserProfile.objects.get(user__id=request.user.id)
            if user is not None:
                serializer = self.serializer_class(user, context={"request": request})
                return Response({"status": "OK", "message": "Successfully fetched user details", "data": serializer.data})

        except UserProfile.DoesNotExist:
            return Response({"status": "FAIL", "message": "User not found", "data": []})


class ProfileUpdateView(MyAPIView):
    
    serializer_class = UserUpdateDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, format=None):
        """
        PUT method to update the data
        """

        if request.user.is_authenticated:

            user_check = get_user_model().objects.filter(pk=request.user.id).exists()

            if not user_check:
                return Response({"status": "FAIL", "message": "User not found", "data": []})

            user = get_user_model().objects.get(pk=request.user.id)

            serializer = UserUpdateDetailsSerializer(user, data=request.data, partial=True, context={"request": request})

            if serializer.is_valid():
                serializer.save()
                return Response({"status": "OK", "message": "Account updated successfully", "data": serializer.data})

            else:
                return Response({"status": "FAIL", "message": "Serializer validation error", "data": serializer.errors})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})
