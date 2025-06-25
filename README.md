echo "# 🛒 Order Processing System

A simplified backend system for handling customer orders using Flask. Supports user authentication, stock management, mock payments, email confirmations, testing, and Docker deployment.

## ✅ Features
- 🔐 User registration/login (JWT)
- 📦 Product stock validation
- 💳 Mock payment simulation
- 📧 Email confirmation with HTML template
- ⚠️ Error handling
- 🧪 Unit testing
- 🧾 Logging support
- 🐳 Docker-ready



## 🧰 Technologies

- Python + Flask
- Flask-JWT-Extended
- Flask-Mail
- SQLAlchemy
- SQLite (for local testing)
- Docker
- Unittest + Mock

---

## ⚙️ Setup and Create Virtual Environment
<pre> git clone https://github.com/FatimaaAlzahraa/order_processing_system
create .env file 
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt  
testing API in postman  </pre> 

## 🔐 Environment (.env)

<pre> SECRET_KEY=your_secret_key 
SQLALCHEMY_DATABASE_URI=sqlite:///database.db 
MAIL_SERVER=smtp.gmail.com 
MAIL_PORT=587 
MAIL_USE_TLS=True 
MAIL_USERNAME=your_email@gmail.com 
MAIL_PASSWORD=your_app_password 
SENDER_EMAIL=your_email@gmail.com 
SENDER_PASSWORD=your_app_password </pre>


## ▶️ Run App

<pre> flask run </pre>


## 🐳 Docker
### Build Docker Image
<pre> <https://hub.docker.com/r/fatmaalzahra/hey-app-flask>
docker build -t order-app .
### Run Docker Container
docker run -p 5000:5000 order-app 
</pre>