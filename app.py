from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from blacklist import BLACKLIST
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserLogin, UserLogout, UserRegister

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'  # Define o banco
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa os warning
app.config['JWT_SECRET_KEY'] = 'SECRET'  # Uma key de criptografia
app.config['JWT_BLACKLIST_ENABLED'] = True  # BLACKLIST dos token
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_database():
    banco.create_all()


@jwt.token_in_blacklist_loader
def create_blacklist(token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def invalid_token():
    return jsonify({'message': 'You have been logged out'}), 401


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:nome>', '/hoteis/<int:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
