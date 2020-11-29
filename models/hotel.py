from sql_alchemy import banco
import sqlite3


class HotelModel(banco.Model):
    __tablename__ = 'hoteis'
    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String)
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String)

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }

    @classmethod
    def find_hotel(cls, parametro):
        if type(parametro) == str:
            hotel = cls.query.filter_by(nome=parametro).first()
        else:
            hotel = cls.query.filter_by(hotel_id=parametro).first()
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()

    def normalize_path_params(cidade=None, estrelas_min=0,
                              estrelas_max=5, diaria_min=0,
                              diaria_max=10000, limit=50, 
                              offset=0, **dados):
        if cidade:
            return{
                'estrelas_min': estrelas_min,
                'estrelas_max': estrelas_max,
                'diaria_min': diaria_min,
                'diaria_max': diaria_max,
                'cidade': cidade,
                'limit': limit,
                'offset': offset
            }
        return {
                'estrelas_min': estrelas_min,
                'estrelas_max': estrelas_max,
                'diaria_min': diaria_min,
                'diaria_max': diaria_max,
                'limit': limit,
                'offset': offset
        }

    def consulta_com_filtros(parametros):
        connection = sqlite3.connect('api.db')
        cursor = connection.cursor()

        if not parametros.get('cidade'):
            consulta = "SELECT * FROM hoteis \
            WHERE (estrelas >= ? and estrelas <= ?) \
            and (diaria >= ? and diaria <= ?) \
            LIMIT ? OFFSET ?"

            tupla_parametros = tuple([parametros[chave]
                                     for chave in parametros])
            resultado = cursor.execute(consulta, tupla_parametros)
        else:
            consulta = "SELECT * FROM hoteis \
            WHERE (estrelas >= ? and estrelas <= ?) \
            and (diaria >= ? and diaria <= ?) \
            and cidade = ? LIMIT ? OFFSET ?"

            tupla_parametros = tuple([parametros[chave]
                                     for chave in parametros])
            resultado = cursor.execute(consulta, tupla_parametros)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4]
            })

        return hoteis
