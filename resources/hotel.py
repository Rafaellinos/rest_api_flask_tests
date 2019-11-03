from flask_restful import Resource, reqparse
from models.hotel import HotelModel


class Hoteis(Resource):
    #Primeiro recurso da API,
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} #query.all SELECT
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