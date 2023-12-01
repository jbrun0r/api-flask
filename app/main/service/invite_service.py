from .. import db
from ..model import User
from ..util.api_error import APIError
from ..service.auth_service import generate_email_validation_token
from ..service.email_service import send_email


def invite_user(data: dict, user):
    """
    Invite a user to join.

    Args:
        data (dict): User data for the invitation.
        user: The user sending the invitation.

    Raises:
        APIError: If the user already exists and is active or if the user already exists.

    Returns:
        dict: The modified user data.
    """

    if User.query.filter_by(email=data["email"]).first():
        if user.activation_status:
            raise APIError("User already exists and is active.", code=409, api_code="USER_ALREADY_ACTIVE")
        else:
            raise APIError("User already exists.", code=409, api_code="USER_ALREADY_EXISTS")

    send_email(
        email=data["email"],
        template_name="USER_VALIDATION.html",
        message_subject="Token User Validation",
        token_student_validation=generate_email_validation_token([data["email"], user.email]),
    )

    return data
