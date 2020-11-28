from blacklist import BLACKLIST
from flask_jwt_extended import create_access_token, get_raw_jwt, jwt_required
from flask_restful import Resource, reqparse
from models.usuario import UserModel
from werkzeug.security import safe_str_cmp

atributos = reqparse.RequestParser()
atributos.add_argument('email', type=str, required=True,
                       help="Cannot be empty.")
atributos.add_argument('senha', type=str, required=True, 
                       help="Cannot be empty.")


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'Message': 'Not Found!'}, 404

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except Exception:
                return {'Message': 'An internal error occurred!'
                        'Please try again!'}, 500
            return {'Message': 'Hotel deleted!'}, 200

        return {'Message': 'Hotel not found!'}, 404


class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_email(dados['email']):
            return {'Message': 'Email already registered'}, 400

        user = UserModel(**dados)
        user.save_user()
        return {'Message': 'User created successfully!'}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_email(dados['email'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token = create_access_token(identity=user.user_id)
            return {'Token': token}
        return {'Message': 'Email or password is incorrect'}


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'Message': 'Logout successfully!'}, 200
