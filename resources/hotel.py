from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.hotel import HotelModel


path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if
                         dados[chave] is not None}

        parametros = HotelModel.normalize_path_params(**dados_validos)
        return {"hoteis": HotelModel.consulta_com_filtros(parametros)}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True,
                            help='Cannot be empty')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade', type=str, required=True,
                            help='Cannot be empty')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'Message': 'Not Found!'}, 404

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'Message': 'Hotel already exists!'}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except Exception:
            return {'Message': 'An internal error occurred!'
                    'Please try again!'}, 500

        return hotel.json()

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.update_hotel(**dados)
            try:
                hotel.save_hotel()
            except Exception:
                return {'Message': 'An internal error occurred!'
                        'Please try again!'}, 500
            return hotel.json(), 200

        novo_hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except Exception:
            return {'Message': 'An internal error occurred!'
                    'Please try again!'}, 500
        return novo_hotel.json(), 201

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except Exception:
                return {'Message': 'An internal error occurred!'
                        'Please try again!'}, 500
            return {'Message': 'Hotel deleted!'}, 200

        return {'Message': 'Hotel not found!'}, 404
