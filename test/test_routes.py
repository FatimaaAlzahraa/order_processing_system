import unittest
from app import create_app, db
from app.models import User, Product

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            product = Product(name='Test Product', price=10.0, stock=5)
            db.session.add(product)
            db.session.commit()

    def test_register_user(self):
        res = self.client.post('/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '123456'
        })
        self.assertEqual(res.status_code, 201)

    def test_place_order_unauthenticated(self):
        res = self.client.post('/order', json={
            'product_id': 1,
            'quantity': 1,
            'email': 'a@a.com'
        })
        self.assertEqual(res.status_code, 401)

if __name__ == '__main__':
    unittest.main()
