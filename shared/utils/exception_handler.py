from django.db.utils import IntegrityError
from rest_framework import exceptions

from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    errors = []
    message = "Internal Server Error"
    status_code = 500

    print(response)
    if response is not None:
        errors = response.data
        message = response.status_text
        status_code = response.status_code
        response = Response({"errors": errors, "message": message}, status=status_code)
    else:
        if isinstance(exc, exceptions.APIException):
            if exc.status_code == 500:
                response = Response(
                    status=status_code, data={"errors": exc.detail, "message": message}
                )
        if isinstance(exc, IntegrityError):
            message = "Bad request"
            response = Response(
                {
                    "errors": ["An entry with similar details already exists"],
                    "message": message,
                },
                status=400,
            )

    return response
