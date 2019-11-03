from sql_alchemy import banco

class HotelModel(banco.Model): #define que cada nome será uma coluna
    __tablename__ = 'hotel'
    #representa o modelo no banco
    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=1))
    cidade = banco.Column(banco.String(40))

    #init da classe
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
    #transforma em dict
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        #cls pega metodo da classe, metodo presente na classe estendiada banco.Model
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() #SELECT * FROM hoteis WHERE hotel_id==hotel_id limite=1
        if hotel:
            return hotel
        return False

    def save_hotel(self): #sava os dados no bd
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade): #update dos dados pra classe
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
