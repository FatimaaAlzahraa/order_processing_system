from flask import Blueprint, request, jsonify , current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from . import db
import os
from dotenv import load_dotenv
from .models import Product, Order, User
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from flask_mail import Message
from . import mail

load_dotenv()
main = Blueprint('main', __name__)

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401


@main.route("/order", methods=["POST"])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.json
    product = Product.query.get(data["product_id"])

    if not product or product.stock < data["quantity"]:
        return jsonify({"error": "Insufficient stock"}), 400

    total = product.price * data["quantity"]
    order = Order(
        product_id=product.id,
        user_id=user_id,
        quantity=data["quantity"],
        total=total,
        paid=True,
        customer_email=data["email"]
    )
    db.session.add(order)
    product.stock -= data["quantity"]
    db.session.commit()

    response = send_confirmation_email(order, product)
    if response:
        return response

    return jsonify({"message": "Order placed successfully", "order_id": order.id})


def send_confirmation_email(order, product):
    try:
        # subject = f"Order Confirmation - Order #{order.id}"

        body = f"""
        Thank you for your order!
        Order ID: {order.id}
        Product: {product.name}
        Quantity: {order.quantity}
        Total: ${order.total}
        """

        msg = Message(
            # subject=subject,
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[order.customer_email],
            body=body
        )

        mail.send(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email failed: {e}")
        return jsonify({"error": "Email failed", "details": str(e)}), 500