import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
MAIL_USERNAME = os.getenv("SENDER_EMAIL")
MAIL_PASSWORD = os.getenv("SENDER_PASSWOR")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") == "True"
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587


