from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from flask_sqlalchemy import SQLAlchemy
import os

# ---- OpenTelemetry imports (Tracing) ----
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


# ----------------------------------
# Read environment variables
# ----------------------------------
DEBUG = os.getenv("DEBUG", "false") == "true"
FLASK_ENV = os.getenv("FLASK_ENV", "production")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

print("🎯 Flask Environment:", FLASK_ENV)
print("🎯 Debug Mode:", DEBUG)
print("🎯 Log Level:", LOG_LEVEL)


# ----------------------------------
# Flask App Init
# ----------------------------------
app = Flask(__name__)


# ----------------------------------
# OpenTelemetry Tracing Setup
# ----------------------------------
trace.set_tracer_provider(TracerProvider())

otlp_exporter = OTLPSpanExporter(
    endpoint="http://tempo.monitoring:4318/v1/traces"
)

span_processor = BatchSpanProcessor(otlp_exporter)

trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument Flask for tracing
FlaskInstrumentor().instrument_app(app)


# ----------------------------------
# Prometheus Metrics
# ----------------------------------
metrics = PrometheusMetrics(app)

metrics.info(
    "app_info",
    "Application info",
    version="1.0.0"
)


# ----------------------------------
# DB variables
# ----------------------------------
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


# ----------------------------------
# SQLAlchemy connection
# ----------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{DB_USER}:{DB_PASS}"
    f"@{DB_HOST}:5432/{DB_NAME}?sslmode=require"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ----------------------------------
# Example model
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

        db.session.execute("SELECT 1")

        return "Healthy", 200

    except Exception as e:

        return f"Unhealthy: {str(e)}", 500
