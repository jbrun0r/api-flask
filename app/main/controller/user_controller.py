from flask import request
from flask_restx import Resource

from ..dto.user_dto import UserDTO
from ..service.user_service import (deactivate_user, delete_user,
                                    update_user, save_new_user, get_all_users,
                                    find_user_by)
from ..dto.pagination_dto import PaginationDTO                                    

api = UserDTO.api
_user = UserDTO.user
_user_post = UserDTO.user_post
_user_get = UserDTO.user_get
_user_put = UserDTO.user_put
_pagination_parser = PaginationDTO.pagination_parser
_user_filters_parser = UserDTO.user_filters_parser
_user_paged = UserDTO.user_paged


@api.route("/")
class UserResource(Resource):
    @api.doc(responses={
        200: "Success",
        404: "`USER_NOT_FOUND` `PAGES_NOT_FOUND`"
    })
    @api.expect(_pagination_parser, _user_filters_parser, validate=True)
    @api.marshal_list_with(_user_paged, code=200, description="List of registered users")
    def get(self):
        """List all registered users."""
        return get_all_users(), 200

    @api.response(204, "User deleted")
    def delete(self, user):
        """Delete self user"""
        return delete_user(user), 204
    
    @api.expect(_user_post, validate=True)
    @api.doc(responses={
        201: "User successfully created",
        406: "`INVALID_CPF`",
        409: "`USER_ALREADY_EXISTS`"
    })
    @api.marshal_with(_user, code=201, description="User successfully created")
    def post(self):
        """Create a new User."""
        data = request.json
        return save_new_user(data=data), 201


@api.route("/<int:id>")
class UserByIdResource(Resource):
    @api.expect(_user_put, validate=True)
    @api.marshal_with(_user)
    def put(self, id: int):
        """Update user by id"""
        data = request.json
        return update_user(data, id=id), 200
    
    @api.doc("registered student by id", responses={
        403: "USER_FORBIDDEN_ACCESS",
        404: "USER_NOT_FOUND"
    })
    @api.marshal_list_with(_user)
    def get(self, id: int):
        """Get a registered user by id"""
        return find_user_by(id=id), 200
