from .. import db
from ..util.api_error import APIError
from ..model import User
from ..service.email_service import send_email
from ..util.pagination_utils import paginate, get_user_filters
from pycpfcnpj.cpfcnpj import validate


def find_user_by(**user_attr) -> User:
    """
    Find a user by specified attributes.

    Args:
        **user_attr: User attributes to filter by.

    Returns:
        User: The found user.

    Raises:
        APIError: If the user is not found.
    """
    if user := User.query.filter_by(**user_attr).first():
        return user
    raise APIError(
        "User doesn't exist.",
        code=404,
        api_code="USER_NOT_FOUND",
        info=f"User not found by params {user_attr}",
    )


def save_new_user(data: dict, skip_commit: bool = False) -> User:
    """
    Save a new user.

    Args:
        data (dict): User data.
        skip_commit (bool): Whether to skip committing to the database.

    Returns:
        User: The newly created user.

    Raises:
        APIError: If the user already exists.
    """
    if not validate(data["cpf"]):
        raise APIError("The CPF provided is not valid.", code=406, api_code="INVALID_CPF")

    if User.query.filter_by(cpf=data["cpf"]).first():
        raise APIError("User already exists.", code=409, api_code="USER_ALREADY_EXISTS")

    user = User(**data)
    if not skip_commit:
        db.session.add(user)
        db.session.commit()

    return user


def update_user(data: dict, id: int) -> User:
    """
    Update a user's information.

    Args:
        data (dict): Updated user data.
        id (int): The user to update.

    Returns:
        User: The updated user.
    """
    if not validate(data["cpf"]):
        raise APIError("The CPF provided is not valid.", code=406, api_code="INVALID_CPF")
    
    user = find_user_by(id=id)
    
    for attribute, new_value in data.items():
        setattr(user, attribute, new_value)
    db.session.commit()
    return user


def update_user_password(data: dict, user: User):
    """
    Update a user's password.

    Args:
        data (dict): Password update data.
        user (User): The id of user to update.

    Raises:
        APIError: If the password doesn't match or is invalid.
    """
    if data["new_password"] != data["confirm_password"]:
        raise APIError("Password doesn't match", code=400, api_code="WRONG_CONFIRM_PASSWORD")
    db.session.commit()


def deactivate_user(id: int, user_agent: User):
    """
    Deactivate a user.

    Args:
        id (int): The ID of the user to deactivate.
        user_agent (User): The user making the request.

    Raises:
        APIError: If the user is not allowed to deactivate the target user.
    """
    user_target = find_user_by(id=id)
    if (
        user_agent.id == user_target.id
        or (user_agent.profile == _USER and user_agent.id == user_target.id)
    ):
        raise APIError("Cannot deactivate user.", code=403, api_code="DEACTIVATE_FORBIDDEN")
    user_target.activation_status = False
    db.session.commit()


def delete_user(id: int):
    """
    Delete a user from the database.

    Args:
        id (int): The id of user to delete.
    """
    user = find_user_by(id=id)

    db.session.delete(user)
    db.session.commit()


def generate_reset_password_email(data: dict):
    """
    Generate and send a reset password email.

    Args:
        data (dict): Email data.
    """
    if find_user_by(email=data["email"]):
        send_email(
            email=data["email"],
            template_name="RESET_PASSWORD.html",
            message_subject="Token Reset Password",
            token_reset_password=f"{generate_email_validation_token(data['email'])}",
        )


def reset_password(data: dict, token: str):
    """
    Reset a user's password.

    Args:
        data (dict): Password reset data.
        token (str): The reset password token.

    Raises:
        APIError: If the password doesn't match or the user is not found.
    """
    email = decode_email_validation_token(token)
    if data["password"] != data["confirm_password"]:
        raise APIError("Password doesn't match", code=400, api_code="WRONG_CONFIRM_PASSWORD")

    user = find_user_by(email=email)
    user.password = generate_hashed_password(data["password"])
    db.session.commit()


def get_all_users():
    """
    Get a paginated list of all users.

    Returns:
        Pagination: Paginated list of Users objects.
    """
    users_filter = get_user_filters()
    return paginate(User, filter=users_filter)
