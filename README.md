# 🛒 Order Processing System

A simple Flask backend to handle product ordering, payments (mock), email confirmations, and JWT-based authentication.

## 🚀 Setup

1. Clone the repo
2. Create `.env` file with:
   - `SECRET_KEY=...`
   - `SQLALCHEMY_DATABASE_URI=sqlite:///app.db`
   - (Mail settings...)
3. Run:

```bash
pip install -r requirements.txt
python run.py
