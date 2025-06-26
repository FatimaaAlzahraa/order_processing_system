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



### Prerequisites
- Python 3.8+
- Docker 
- Gmail account for email service

echo "## 🚀 Setup Instructions

### 🔹 Clone and Install Dependencies

### 🔹 Clone and Install Dependencies

<pre>
git clone https://github.com/FatimaaAlzahraa/order_processing_system
cd order_processing_system
python -m venv venv
# For Windows:
venv\Scripts\activate
# For Mac/Linux:
source venv/bin/activate
pip install -r requirements.txt
</pre>


---

## 🔐 Configuration

Create a \`.env\` file with the following:

<p>
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_here
SQLALCHEMY_DATABASE_URI=sqlite:///database.db
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
<P>

---

## 🗃️ Initialize Database

<P>
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
<P>

---

## 🧪 Run Tests

<P>
python -m unittest discover -s tests
<P>

---

## ▶️ Run the Application

<p>
flask run
<P>

---

## 🐳 Docker Deployment

### 🔹 Docker Hub

- 📦 [View the Image on Docker Hub](https://hub.docker.com/r/fatmaalzahra/hey-app-flask)

### 🔹 Build Docker Image

\`\`\`bash
docker build -t fatmaalzahra/hey-app-flask .
\`\`\`

### 🔹 Run Docker Container

\`\`\`bash
docker run -p 5000:5000 fatmaalzahra/hey-app-flask
\`\`\`" 
