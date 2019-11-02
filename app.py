from flask import Flask
from flask_restful import Resource, Api

from resources.hotel import Hoteis, Hotel #chamando class hotel em pasta resource e arquivo hotel

app = Flask(__name__)
api = Api(app) #faz o gerenciamento


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

if __name__ == '__main__': #flask se nome form principal, rode
    app.run(debug=True)
# http://127.0.0.1:5000/hoteis
