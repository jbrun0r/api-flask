from flask_restx import Namespace, fields, inputs

from .pagination_dto import PaginationDTO


email_pattern = r"^(?:[\w]+|([-_.])(?!\1))+@+(?:[\w]+|([-_.])(?!\1))(\.[\w]{2,10})+$"
phone_number_pattern = r"^$|^[1-9]{2}(?:[2-8]|9[1-9])[0-9]{3}[0-9]{4}$"


class UserDTO:
    api = Namespace("user", description="User related operations")

    user_filters_parser = api.parser()
    user_filters_parser.add_argument("search", type=str, location="query")
    user_filters_parser.add_argument("name", type=str, location="query")
    user_filters_parser.add_argument("cpf",type=inputs.regex(r"(^\d{11}$)"), location="query",)
    user_filters_parser.add_argument("age", type=str, location="query")

    user_put = api.model(
        "UserPut",
        {
            "name": fields.String(
                required=True,
                description="User's full name",
                max_length=80,
                example="João Bruno Rodrigues"
            ),
            "cpf": fields.String(
                required=True,
                description="User cpf",
                max_length=11,
                pattern=r"^\d{11}$",
                example="07329815473",
            ),
            "age": fields.String(
                required=True,
                description="User age",
                max_length=3,
                pattern=r"^\d+$",
                example="22",
            ),
        },
        strict=True,
    )

    
    user_post = api.clone(
        "UserPost",
        user_put,
    )
    user_post.__strict__ = True

    user = api.clone(
        "User",
        {
            "id": fields.Integer(required=False),
        },
        user_post,
    )

    user_get = api.clone(
        "UserGet",
        user,
    )

    user_auth = api.inherit(
        "UserAuth",
        user,
    )

    user_paged = api.clone(
        "UserPaged",
        PaginationDTO.pagination_base,
        {
            "items": fields.List(fields.Nested(user)),
        },
    )
