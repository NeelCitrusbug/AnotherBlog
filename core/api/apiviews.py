# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView

from .response import MyAPIResponse
from core.utils import modify_api_response

# -----------------------------------------------------------------------------


class MyObtainAuthToken(ObtainAuthToken):
    """
    Override ObtainAuthToken to add in user ID.
    """

    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return MyAPIResponse(data={"user": user.pk, "token": token.key})


class MyAPIView(APIView):
    def finalize_response(self, request, response, *args, **kwargs):
        # Override response (is there a better way to do this?)
        response = modify_api_response(response)
        return super().finalize_response(request, response, *args, **kwargs)


class MyGenericAPIView(generics.GenericAPIView):
    def finalize_response(self, request, response, *args, **kwargs):
        # Override response (is there a better way to do this?)
        response = modify_api_response(response)
        return super().finalize_response(request, response, *args, **kwargs)


class MyUpdateAPIView(mixins.UpdateModelMixin, MyGenericAPIView):
    """
    UpdateAPIView
    UpdateModelMixin
    GenericAPIView
    APIView
    View
    """

    pass


class MyListAPIView(generics.ListAPIView):
    def finalize_response(self, request, response, *args, **kwargs):
        # Override response (is there a better way to do this?)
        response = modify_api_response(response)
        return super().finalize_response(request, response, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        #    return self.get_paginated_response(serializer.data)
            return Response({"message": "Successfully fetched data", "data": self.get_paginated_response(serializer.data)})

        serializer = self.get_serializer(queryset, many=True)
        return Response({"message": "Successfully fetched data", "data": serializer.data})
