from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def connect_db(app):
    '''connect to database.'''
    db.app = app
    db.init_app(app)


class Cupcake(db.Model):

    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    flavor = db.Column(db.String(50),
                       nullable=False)
    size = db.Column(db.String(30),
                     nullable=False)
    rating = db.Column(db.Float,
                       nullable=False)
    image = db.Column(db.Text,
                      server_default='https://tinyurl.com/truffle-cupcake')
    
    def serialize(self):
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }
        