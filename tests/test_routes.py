import unittest
from unittest.mock import patch
from app import create_app, db
from app.models import User, Product
from flask_jwt_extended import create_access_token

class OrderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            # Create test user
            user = User(username="buyer", email="buyer@example.com")
            user.set_password("123456")
            db.session.add(user)

            # Create test product
            product = Product(name="TestProduct", price=20.0, stock=5)
            db.session.add(product)

            db.session.commit()
            self.user_id = user.id
            self.token = create_access_token(identity=user.id)

    @patch('app.routes.send_confirmation_email')  # mock email sending
    def test_authenticated_order_success(self, mock_send_email):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = self.client.post('/order', json={
            'product_name': 'TestProduct',
            'quantity': 2,
            'email': 'buyer@example.com'
        }, headers=headers)

        self.assertEqual(response.status_code, 422)
        self.assertIn('order_id', response.get_json())
        mock_send_email.assert_called_once()

    def test_unauthenticated_order(self):
        response = self.client.post('/order', json={
            'product_name': 'TestProduct',
            'quantity': 2,
            'email': 'buyer@example.com'
        })
        self.assertEqual(response.status_code, 401)

    def test_invalid_product(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.post('/order', json={
            'product_name': 'InvalidName',
            'quantity': 2,
            'email': 'buyer@example.com'
        }, headers=headers)
        self.assertEqual(response.status_code, 422)
        self.assertIn('error', response.get_json())

    def test_insufficient_stock(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.post('/order', json={
            'product_name': 'TestProduct',
            'quantity': 10,
            'email': 'buyer@example.com'
        }, headers=headers)
        self.assertEqual(response.status_code, 422)
        self.assertIn('error', response.get_json())

if __name__ == '__main__':
    unittest.main()

