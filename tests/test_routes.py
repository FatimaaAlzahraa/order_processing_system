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
        self.app.config['JWT_SECRET_KEY'] = 'test-secret-key'  # Add JWT config for testing

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
            self.token = create_access_token(identity=str(user.id))  # Ensure string identity

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('app.routes.send_confirmation_email')
    def test_authenticated_order_success(self, mock_send_email):
        mock_send_email.return_value = None  # Mock successful email
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.post('/order', json={
            'product_name': 'TestProduct',
            'quantity': 2,
            'email': 'buyer@example.com'
        }, headers=headers)

        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn('order_id', response_data)
        self.assertIn('product_name', response_data)
        self.assertEqual(response_data['quantity'], 2)
        mock_send_email.assert_called_once()

    def test_unauthenticated_order(self):
        response = self.client.post('/order', json={
            'product_name': 'TestProduct',
            'quantity': 2,
            'email': 'buyer@example.com'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('msg', response.get_json())  # JWT error message

    def test_invalid_product(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.post('/order', json={
            'product_name': 'InvalidName',
            'quantity': 2,
            'email': 'buyer@example.com'
        }, headers=headers)
        self.assertEqual(response.status_code, 404)
        response_data = response.get_json()
        self.assertIn('error', response_data)
        self.assertIn('message', response_data)

    def test_insufficient_stock(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.post('/order', json={
            'product_name': 'TestProduct',
            'quantity': 10,
            'email': 'buyer@example.com'
        }, headers=headers)
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertIn('error', response_data)
        self.assertIn('available_stock', response_data)
        self.assertEqual(response_data['available_stock'], 5)

    def test_missing_fields(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.post('/order', json={
            'product_name': 'TestProduct',
            'quantity': 2
            # Missing email
        }, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

if __name__ == '__main__':
    unittest.main()
