from app import app
from models import db, connect_db, Cupcake
import unittest

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes-app-test'
connect_db(app)

class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client and make new cupcake."""

        #create tables
        db.create_all()

        self.client = app.test_client()

        self.new_cupcake = Cupcake(
            flavor='testing', size='small', rating=10)
        self.new_cupcake2 = Cupcake(
            flavor='testing2', size='medium', rating=10)
    
        db.session.add(self.new_cupcake)
        db.session.add(self.new_cupcake2)
        db.session.commit()

    def tearDown(self):
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        db.drop_all(bind=None)

    def test_root(self):

        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        
    def test_all_cupcakes(self):

        response = self.client.get('/cupcakes')
        self.assertEqual(response.status_code, 200)
        print(response.json['cupcakes'])
        self.assertEqual(response.json['cupcakes'],
                         [self.new_cupcake.serialize(), self.new_cupcake2.serialize()])


    def test_add_cupcake(self):

        # self.assertEqual(Cupcake.query.count(), 1)
        response = self.client.post('/cupcakes', json={
            'flavor': 'new_cupcake', 'size': 'small', 'rating': 10
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['cupcake'],
                         {'id':3,  'flavor': 'new_cupcake', 'size': 'small', 'rating': 10, 'image': 'https://tinyurl.com/truffle-cupcake'})

