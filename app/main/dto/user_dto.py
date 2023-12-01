from flask_restx import Namespace, fields, inputs

from .pagination_dto import PaginationDTO


id_pattern = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"

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
            "id": fields.String(
                required=False,
                pattern=id_pattern,
                example="828666de-a8b9-43c9-86c8-767449a0fcbe"),
        },
        user_post,
    )


    user_paged = api.clone(
        "UserPaged",
        PaginationDTO.pagination_base,
        {
            "items": fields.List(fields.Nested(user)),
        },
    )
