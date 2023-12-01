from flask import request
from flask_restx import Resource

from ..dto.user_dto import UserDTO
from ..service.user_service import (deactivate_user, delete_user,
                                    update_user, save_new_user)

api = UserDTO.api
_user = UserDTO.user
_user_post = UserDTO.user_post
_user_get = UserDTO.user_get
_user_put = UserDTO.user_put


@api.route("/")
@api.doc(responses={
    404: "USER_NOT_FOUND",
})
class UserResource(Resource):
    @api.marshal_with(_user_get)
    def get(self, user):
        """get self logged"""
        return user, 200

    @api.expect(_user_put, validate=True)
    @api.marshal_with(_user)
    def put(self, user):
        """Change self profile"""
        data = request.json
        return update_user(data, user), 200

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
    @api.doc("User deactivate operations", responses={
        204: "User deactivated",
        401: "INVALID_TOKEN|EXPIRED_TOKEN|DECODED_USER_NOT_FOUND|TOKEN_IS_MISSING",
        403: "PROFILE_FORBIDDEN_ACCESS|DEACTIVATE_FORBIDDEN",
        404: "USER_NOT_FOUND",
    })
    def put(self, id: int, user):
        """Deactivate User by id"""
        return deactivate_user(id, user), 204
