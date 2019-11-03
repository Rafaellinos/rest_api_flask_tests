from flask_restful import Resource, reqparse
from models.usuario import UserModel

class User(Resource):

    #pega os argumentos vindos da requisição Json
    """
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help='The field name cannot be blank')
    argumentos.add_argument('estrelas', type=float, required=True, help='The field estrelas cannot be blank')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    """
    def get(self, user_id):
        user = UserModel.find_hotel(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404 #status errado


    def delete(self, user_id):
        #para cada hotel na lista, retorna hoteis que não forem iguais ao hotel passado por parâmetro
        #basicamente cria-se uma lista nova sem o hotel passado por parâmetro.
        #global #hoteis Necessário para infromar ao python que hoteis não é a mesma usada na lista
        #hoteis = [hotel for hotel in hoteis if hotel['user_id'] != user_id]
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocurred trying to delete user.'}, 500 #intel server error
            return {'message': 'User deleted'}, 200
        return {'message': 'User not found.'}, 404