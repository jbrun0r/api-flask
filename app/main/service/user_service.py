from .. import db
from ..util.api_error import APIError
from ..model import User
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


def delete_user(id: int):
    """
    Delete a user from the database.

    Args:
        id (int): The id of user to delete.
    """
    user = find_user_by(id=id)

    db.session.delete(user)
    db.session.commit()


def get_all_users():
    """
    Get a paginated list of all users.

    Returns:
        Pagination: Paginated list of Users objects.
    """
    users_filter = get_user_filters()
    return paginate(User, filter=users_filter)
