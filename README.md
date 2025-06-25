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

## 📁 Project Structure
\`\`\`
app/
├── routes.py
├── models.py
├── templates/
│   └── confirmation_email.html
tests/
├── test_auth.py
├── test_order.py
.env
config.py
requirements.txt
run.py
Dockerfile
\`\`\`

## ⚙️ Setup

\`\`\`bash
git clone <https://github.com/FatimaaAlzahraa/order_processing_system>
cd order_process_sys
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

## 🔐 Environment (.env)

\`\`\`
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///database.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
\`\`\`

## ▶️ Run App

\`\`\`bash
flask run
\`\`\`



