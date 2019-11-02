from flask import Flask
from flask_restful import Resource, Api

from resources.hotel import Hoteis, Hotel #chamando class hotel em pasta resource e arquivo hotel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app) #faz o gerenciamento

@app.before_first_request
def cria_banco():
    banco.create_all()

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

if __name__ == '__main__': #flask se nome form principal, rode
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
# http://127.0.0.1:5000/hoteis
