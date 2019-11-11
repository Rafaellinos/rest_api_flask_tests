from sql_alchemy import banco

class SiteModel(banco.Model): #define que cada nome será uma coluna
    __tablename__ = 'sites'
    #representa o modelo no banco
    
    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel') #lista de obj hoteis que sao consultados automaticamente

    #init da classe
    def __init__(self, url):
        self.url = url
    #transforma em dict
    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis],
        }

    @classmethod
    def find_site(cls, url):
        #cls pega metodo da classe, metodo presente na classe estendiada banco.Model
        site = cls.query.filter_by(url=url).first()
        if site:
            return site
        return False

    def save_site(self): #sava os dados no bd
        banco.session.add(self)
        banco.session.commit()

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
