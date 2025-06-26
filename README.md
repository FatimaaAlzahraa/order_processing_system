# 🛒 Order Processing System

A Flask-based e-commerce backend with JWT authentication, order processing, and email confirmations. Ready for Docker deployment.

![Docker Image](https://img.shields.io/docker/pulls/fatmaalzahra/hey-app-flask) 
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

## 🌟 Features

- 🔐 JWT Authentication (Register/Login)
- 📦 Product inventory management
- 💳 Order processing with stock validation
- ✉️ Email confirmation system
- 🧪 Comprehensive unit testing
- 🐳 Docker container support
- 📝 HTML templates for web interface
- ⚡ REST API endpoints

## 🛠️ Technologies

| Component          | Technology               |
|--------------------|--------------------------|
| Framework          | Flask                    |
| Authentication     | Flask-JWT-Extended       |
| Database           | SQLAlchemy + SQLite      |
| Email              | Flask-Mail + SMTP        |
| Testing            | unittest + Mock          |
| Deployment         | Docker                   |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker (optional)
- Gmail account for email service

### Installation
```bash
git clone https://github.com/FatimaaAlzahraa/order_processing_system
cd order_processing_system
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt


##  Configuration

Create `.env` file:
```ini
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_here
SQLALCHEMY_DATABASE_URI=sqlite:///database.db
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password


Initialize Database
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()

Running the Application
flask run

🐳 Docker Deployment
docker pull fatmaalzahra/hey-app-flask
docker run -p 5000:5000 fatmaalzahra/hey-app-flask

Build Locally
docker build -t order-processing-system .
docker run -p 5000:5000 order-processing-system

Testing
python -m unittest discover -s tests
