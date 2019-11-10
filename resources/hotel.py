from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

def normalize_path_params(cidade=None,
                          estrelas_min = 0,
                          estrelas_max = 5,
                          diaria_min = 0,
                          diaria_max = 10000,
                          limit = 50,
                          offset = 0,
                          **dados):
    if cidade:
        return {
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

# path /hoteis?cidade=Rio de Janeiro&estrelas_min4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    #Primeiro recurso da API,
    def get(self):
        connection = sqlite3.connect('banco.db') #conecta ao banco
        cursor = connection.cursor()

        dados = path_params.parse_args()
        #apenas dados válidos
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos) #devolve valores normalizados(ordem, com cidade ou sem cidade)
        if not parametros.get('cidade'): #se tiver cidade
            consulta = "SELECT * FROM hotel " \
                       "WHERE (estrelas > ? and estrelas < ?) " \
                       "and (diaria > ? and diaria < ?) " \
                       "LIMIT ? OFFSET ?" #query
            tupla = tuple([parametros[chave] for chave in parametros]) #pega só os valores do parâmetro
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = "SELECT * FROM hotel " \
                       "WHERE (estrelas > ? and estrelas < ?) " \
                       "and (diaria > ? and diaria < ?) " \
                       "and cidade = ? LIMIT ? OFFSET ?" #query
            tupla = tuple([parametros[chave] for chave in parametros])  # pega só os valores do parâmetro
            resultado = cursor.execute(consulta, tupla)
        hoteis = []
        for linhas in resultado:
            hoteis.append({
                'hoteil_id': linhas[0],
                'nome': linhas[1],
                'estrelas': linhas[2],
                'diaria': linhas[3],
                'cidade': linhas[4]
            })
        return {'hoteis': hoteis} #query.all SELECT
        #retorna dict, api flask_restful converte em JSON automaticamente

class Hotel(Resource):

    #pega os argumentos vindos da requisição Json
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help='The field name cannot be blank')
    argumentos.add_argument('estrelas', type=float, required=True, help='The field estrelas cannot be blank')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404 #status errado

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists".format(hotel_id)}, 400 #bad request
        dados = Hotel.argumentos.parse_args()
        #dados chave e valor
        hotel_objeto = HotelModel(hotel_id, **dados)
        try:
            hotel_objeto.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 #intel server error

        return hotel_objeto.json(), 201

    @jwt_required
    def put(self, hotel_id):
        #parse dos objetos passados pra classe
        dados = Hotel.argumentos.parse_args()
        #procura no bd o hotel
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            #Se encontrado, update
            hotel_encontrado.update_hotel(**dados)
            try:
                #salva o update no bd
                hotel_encontrado.save_hotel()
            except:
                return {'message': 'An internal error ocurred trying to save hotel.'}, 500 #intel server error
            return hotel_encontrado.json(), 200
        #caso hotel não tenha sido encontrado, salva um novo
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 #intel server error
        return hotel.json(), 201 # created

    @jwt_required
    def delete(self, hotel_id):
        #para cada hotel na lista, retorna hoteis que não forem iguais ao hotel passado por parâmetro
        #basicamente cria-se uma lista nova sem o hotel passado por parâmetro.
        #global #hoteis Necessário para infromar ao python que hoteis não é a mesma usada na lista
        #hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to delete hotel.'}, 500 #intel server error
            return {'message': 'Hotel deleted'}, 200
        return {'message': 'Hotel not found.'}, 404