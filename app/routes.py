from flask import Blueprint, request, jsonify
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
load_dotenv()
main = Blueprint('main', __name__)

# authorization user 
# 1- register 
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

# 2-login
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

# 3- create the order for the user 
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

# 4- send confirm email for the authorized user
def send_confirmation_email(order, product):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = order.customer_email

    # check the presences of email  data 
    if not sender_email or not sender_password:
        return jsonify({"error": "Email credentials are missing"}), 500

    #Words in email 
    subject = f"Order Confirmation - Order #{order.id}"

    html = f"""
    <html>
        <body>
            <h2>Thank you for your order!</h2>
            <p>Order ID: #{order.id}</p>
            <p>{order.quantity} &times; {product.name} = ${order.total}</p>
        </body>
    </html>
    """

    #Setup email
    message = MIMEMultipart()
    message["From"] = formataddr((str(Header("Order Service", "utf-8")), sender_email))
    message["To"] = receiver_email
    message["Subject"] = Header(subject, "utf-8")
    message.attach(MIMEText(html, "html", "utf-8"))

    #Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f" Email sending failed: {e}")
        return jsonify({"error": "Email failed", "details": str(e)}), 500