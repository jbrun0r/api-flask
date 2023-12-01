from .. import db
from ..model import Error
from werkzeug.exceptions import HTTPException


class APIError(HTTPException):
    """
    Custom exception class representing a default or generic error.

    Attributes:
        message (str): Error message (default: "Generic error").
        info (dict): Additional information about the error (default: None).
        code (int): HTTP status code for the error (default: None).
        api_code (str): API-specific error code (default: None).
    """

    def __init__(self, message="Generic error", info=None, code=None, api_code=None):
        """
        Initialize the APIError instance.

        Args:
            message (str, optional): Error message (default: "Generic error").
            info (dict, optional): Additional information about the error (default: None).
            code (int, optional): HTTP status code for the error (default: None).
            api_code (str, optional): API-specific error code (default: None).
        """
        self.code = code
        self.description = message
        self.info = info
        self.api_code = (api_code or message).upper().replace(' ', '_').replace('.', '')

        super().__init__()

    def to_error(self) -> Error:
        """
        Convert the APIError to an Error model instance.

        If an Error instance with the same api_code already exists in the database, update its description.
        Otherwise, create a new Error instance and add it to the database.

        Returns:
            Error: The converted Error model instance.
        """
        if error := Error.query.filter_by(api_code=self.api_code).first():
            error.description = self.description
        else:
            error = Error(
                code=self.code,
                api_code=self.api_code,
                name=self.name,
                description=self.description,
            )
            db.session.add(error)
            db.session.commit()

        if self.info:
            error.info = self.info

        return error
    
    @classmethod
    def add_errors_to_database(cls):
        """
        Add API errors to the database.

        Iterate over the API_ERROR_CODES dictionary and add each error to the database as an Error instance.
        """

        for api_code, api_error in API_ERROR_CODES.items():
            db.session.add(Error(api_code=api_code, **api_error))
        db.session.commit()


API_ERROR_CODES = {
    "INVALID_DATA": {
        "code": 400,
        "name": "Bad Request",
        "description": "Invalid Data.",
    },
    "INVALID_UUID_FORMAT": {
        "code": 400,
        "name": "Bad Request",
        "description": "Invalid UUID format.",
    },
    "PAGES_NOT_FOUND": {
        "code": 404,
        "name": "Not Found",
        "description": "No page generated",
    },
    "USER_NOT_FOUND": {
        "code": 404,
        "name": "Not Found",
        "description": "User doesn't exist.",
    },
    "PAGE_NOT_FOUND": {
        "code": 404,
        "name": "Not Found",
        "description": "Page doesn't exist.",
    },
    "USER_ALREADY_EXISTS": {
        "code": 409,
        "name": "Conflict",
        "description": "User already exists",
    },
    "INVALID_CPF": {
        "code": 406,
        "name": "Not Acceptable",
        "description": "The CPF provided is not valid",
    },
}
