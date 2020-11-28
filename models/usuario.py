from sql_alchemy import banco


class UserModel(banco.Model):
    __tablename__ = 'users'
    user_id = banco.Column(banco.Integer, primary_key=True)
    email = banco.Column(banco.String)
    senha = banco.Column(banco.String)

    def __init__(self, email, senha):
        self.email = email
        self.senha = senha

    def json(self):
        return {
            'user_id': self.user_id,
            'email': self.email
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
