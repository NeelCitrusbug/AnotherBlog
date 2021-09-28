# -*- coding: utf-8 -*-

from rest_framework import mixins, viewsets

# from .utils import get_status
from core.utils import modify_api_response
 

class MyGenericViewSet(viewsets.GenericViewSet):
    """
    Custom API response format.
    """

    def finalize_response(self, request, response, *args, **kwargs):
        # Override response (is there a better way to do this?)
        response = modify_api_response(response)
        return super().finalize_response(request, response, *args, **kwargs)


class MyModelViewSet( 
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    MyGenericViewSet,
):
    """
    Custom API response format.
    """

    pass


class MyCreateViewSet(mixins.CreateModelMixin, MyGenericViewSet):
    """
    Custom API response format.
    """

    pass


class MyCreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, MyGenericViewSet
):
    """
    Custom API response format.
    """

    pass


class MyCreateRetrieveViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, MyGenericViewSet
):
    """
    Custom API response format.
    """

    pass


class MyCreateListRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    MyGenericViewSet,
):
    """
    Custom API response format.
    """

    pass


class MyListViewSet(mixins.ListModelMixin, MyGenericViewSet):
    """
    Custom API response format.
    """

    pass


class MyListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, MyGenericViewSet
):
    """
    Custom API response format.
    """

    pass


class MyRetrieveUpdateViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, MyGenericViewSet
):
    """
    Custom API response format.
    """

    pass


class MyRetrieveViewSet(mixins.RetrieveModelMixin, MyGenericViewSet):
    """
    Custom API response format.
    """

    pass


class MyUpdateViewSet(mixins.UpdateModelMixin, MyGenericViewSet):
    """
    Custom API response format.
    """

    pass

class MyRetrieveUpdateDestroyViewSet( 
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    MyGenericViewSet,
):
    """
    Custom API response format.
    """

    pass

class MyCreateRetrieveUpdateDestroyViewSet( 
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    MyGenericViewSet,
):
    """
    Custom API response format.
    """

    pass

class MyCreateRetrieveUpdateViewSet( 
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, 
    MyGenericViewSet,
):
    """
    Custom API response format.
    """

    pass