from sql_alchemy import banco

class UserModel(banco.Model): #define que cada nome será uma coluna
    __tablename__ = 'usuarios'
    #representa o modelo no banco
    user_id = banco.Column(banco.Integer, primary_key=True) #cria auto incriment automaticamente
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    #init da classe
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    #transforma em dict
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login
        }

    @classmethod
    def find_user(cls, user_id):
        #cls pega metodo da classe, metodo presente na classe estendiada banco.Model
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    def save_user(self): #sava os dados no bd
        banco.session.add(self)
        banco.session.commit()

    def update_user(self, login, senha): #update dos dados pra classe
        self.login = login
        self.senha = senha

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
