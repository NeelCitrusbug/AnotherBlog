# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.response import Response

from core.utils import modify_api_response


def MyAPIResponse(data=None, code=status.HTTP_200_OK):
    """
    Custom API response format.
    """
    return modify_api_response(Response(data, status=code))
