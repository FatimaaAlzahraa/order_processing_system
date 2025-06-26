from flask import Blueprint, request, jsonify
from flask import render_template, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from . import db
import os
from flask import session, redirect, url_for
from dotenv import load_dotenv
from .models import Product, Order, User
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
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
        token = create_access_token(identity=str(user.id))  # Ensure identity is string
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@main.route("/order", methods=["POST"])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()

    # Validate input
    product_name = data.get("product_name")
    quantity = data.get("quantity")
    email = data.get("email")

    if not all([product_name, quantity, email]):
        return jsonify({"error": "Missing required fields", "message": "product_name, quantity, and email are required"}), 400

    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"error": "Invalid quantity", "message": "Quantity must be a number"}), 400

    product = Product.query.filter_by(name=product_name).first()
    if not product:
        return jsonify({"error": "Product not found", "message": f"Product '{product_name}' doesn't exist"}), 404

    if quantity > product.stock:
        return jsonify({
            "error": "Insufficient stock",
            "message": f"Only {product.stock} items available",
            "available_stock": product.stock
        }), 400

    total = product.price * quantity

    try:
        order = Order(
            product_id=product.id,
            user_id=user_id,
            quantity=quantity,
            total=total,
            paid=True,
            customer_email=email
        )

        db.session.add(order)
        product.stock -= quantity
        db.session.commit()

        email_result = send_confirmation_email(order, product)
        if isinstance(email_result, tuple): 
            return email_result

        return jsonify({
            "message": "Order placed successfully",
            "order_id": order.id,
            "product_name": product.name,
            "quantity": quantity,
            "total": total
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Order failed", 
            "message": str(e),
            "details": "Please try again later"
        }), 500

def send_confirmation_email(order, product):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = order.customer_email

    if not sender_email or not sender_password:
        return jsonify({
            "error": "Email service unavailable",
            "message": "Failed to send confirmation email"
        }), 500

    subject = f"Order Confirmation - Order #{order.id}"

    try:
        with current_app.app_context():
            html = render_template('confirmation_email.html', order=order, product=product)

        message = MIMEMultipart()
        message["From"] = formataddr(("Order Service", sender_email))
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(MIMEText(html, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        logging.info(f"Email sent to {receiver_email}")
        return None

    except Exception as e:
        logging.error(f"Email sending failed: {e}")
        return jsonify({
            "error": "Email failed",
            "message": "Confirmation email could not be sent",
            "details": str(e)
        }), 500











# ---------------------------------------------------------------------------------------------------------------------------------

# simple app with html and flask 
@main.route('/')
def landing():
    return render_template('landing.html')

@main.route('/registers', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Username already exists")

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id  # 
        return redirect(url_for('main.home'))  

    return render_template('register.html')


@main.route('/logins', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('main.home'))  # بعد تسجيل الدخول نرجع للهوم
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@main.route('/product')
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@main.route('/place-order', methods=['POST'])
def place_order():
    # ✅ تأكد أن المستخدم سجل الدخول
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.login_page'))

    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    email = request.form['email']

    product = Product.query.get(product_id)
    if not product or product.stock < quantity:
        return "Insufficient stock", 400

    order = Order(
        product_id=product.id,
        user_id=user_id,
        quantity=quantity,
        total=product.price * quantity,
        paid=True,
        customer_email=email
    )

    db.session.add(order)
    product.stock -= quantity
    db.session.commit()

    send_confirmation_email(order, product)
    return render_template('success.html', order=order)


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login_page'))
