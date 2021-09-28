# -*- coding: utf-8 -*-

from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler

from core.utils import get_status


def get_api_error(source, detail, code):
    """
    Return an error object for use in the errors key of the response.
    http://jsonapi.org/examples/#error-objects-multiple-errors
    """
    error_obj = {}
    error_obj["source"] = source
    error_obj["detail"] = detail
    if code:
        error_obj["code"] = code
    return error_obj


def get_clean_errors(data):
    """
    DRF will send errors through as data so let's rework it.
    """
    errors = []
    for k, v in data.items():
        ed = ErrorDetail(v)
        if isinstance(v, list):
            v = ", ".join(v)
        errors.append(get_api_error(source=k, detail=v, code=ed.code))
    return errors


def get_api_error_response(response):
    """
    Custom API error response format.
    {
        "code": 400,
        "status": "BAD_REQUEST",
        "errors": [
            {
                "source": "first_name",
                "detail": "This field may not be blank."
            }
        ]
    }
    """
    modified_data = {}
    modified_data["code"] = response.status_code
    modified_data["status"] = get_status(response.status_code)
    modified_data["errors"] = get_clean_errors(response.data)
    # modified_data["errors"] = response.data
    response.data = modified_data
    return response


def custom_exception_handler(exc, context):
    """
    Custom exception handler.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Create our custom response format
    if response is not None:
        response = get_api_error_response(response)

    return response
