# -*- coding: utf-8 -*-

from django.utils import timezone
from rest_framework import serializers

# -----------------------------------------------------------------------------


class DateTimeTzAwareField(serializers.DateTimeField):
    """
    Ensure UTC time is in our local timezone.
    """

    def to_representation(self, value):
        value = timezone.localtime(value)
        return super().to_representation(value)
