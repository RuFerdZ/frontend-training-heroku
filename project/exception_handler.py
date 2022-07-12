import logging
import re

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from project import settings

logger = logging.getLogger("project.exception_handler")


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    message = type(exc).__name__
    default_error = ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', message))
    if response is not None:
        if isinstance(response.data, list):
            error = response.data
        else:
            error = [response.data.get('detail') if 'detail' in response.data else response.data]
    else:
        response = Response()
        error = [str(exc) if str(exc) != '' else default_error]
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR and settings.DEBUG is True:
        logger.exception(exc)

    response.data = {
        'message': message,
        'errors': error,
        'status': 'failure',
    }

    return response
