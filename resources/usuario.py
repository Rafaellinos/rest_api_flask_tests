from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='The field login cannot be blank')
atributos.add_argument('senha', type=str, required=True, help='The field senha cannot be blank')

class User(Resource):
    # /usuarios/{user_id}
    #pega os argumentos vindos da requisição Json
    """
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help='The field name cannot be blank')
    argumentos.add_argument('estrelas', type=float, required=True, help='The field estrelas cannot be blank')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    """
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404 #status errado

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocurred trying to delete user.'}, 500 #intel server error
            return {'message': 'User deleted'}, 200
        return {'message': 'User not found.'}, 404

class UserRegister(Resource):
    # /cadastro/

    def post(self):
        
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return{'message': "User '{}' already exists".format(dados['login'])}, 200

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created successfully!'}, 201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login']) #busca no banco pelo login
        if user and safe_str_cmp(user.senha, dados['senha']): #faz a validação da string de forma segura
            token_de_acesso = create_access_token(identity=user.user_id) #cria o acess token
            return {'access_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect'}, 401 #unauthorized

class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] # JWT token, Token, Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200