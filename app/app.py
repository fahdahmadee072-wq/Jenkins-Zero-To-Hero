from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# ----------------------------------
# Read environment variables (DevOps injects these)
# ----------------------------------
DEBUG = os.getenv("DEBUG", "false") == "true"
FLASK_ENV = os.getenv("FLASK_ENV", "production")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

print("🎯 Flask Environment:", FLASK_ENV)
print("🎯 Debug Mode:", DEBUG)
print("🎯 Log Level:", LOG_LEVEL)

# Flask App Init
app = Flask(__name__)

# ----------------------------------
# DB variables
# ----------------------------------
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# ----------------------------------
# SQLAlchemy connection string (Azure requires sslmode=require)
# ----------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{DB_USER}:{DB_PASS}"
    f"@{DB_HOST}:5432/{DB_NAME}?sslmode=require"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ----------------------------------
# Example model (developer responsibility)
# ----------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

# ----------------------------------
# Routes
# ----------------------------------
@app.route("/")
def home():
    return "Hello from Flask + NGINX + Azure PostgreSQL!"

@app.route("/health")
def health():
    try:
        # Simple DB check using SQLAlchemy
        db.session.execute("SELECT 1")
        return "Healthy", 200
    except Exception as e:
        return f"Unhealthy: {str(e)}", 500
