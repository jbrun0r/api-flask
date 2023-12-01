from flask import Blueprint
from flask_restx import Api

from .main.controller.error_controller import _error_response, api as error_ns
from .main.controller.user_controller import api as user_ns
from .main.util.api_error import APIError

blueprint = Blueprint("api", __name__)

api = Api(blueprint,
          title="API",
          prefix='/api/',
          version="X.Y.Z",
          description="API",
          security="apikey",
          contact_email="joaobruno.rf@gmail.com",
          )

api.add_namespace(error_ns, path="/error")
api.add_namespace(user_ns, path="/user")


@api.errorhandler(APIError)
@error_ns.marshal_with(_error_response)
def handle_default_exception(error):
    """
    Handles APIError and returns a formatted error response.

    Args:
        error (APIError): The exception to be handled.

    Returns:
        tuple: A tuple containing the formatted error response object and the corresponding HTTP status code.
    """
    if isinstance(error, APIError):
        return {"error": error.to_error()}, error.code
