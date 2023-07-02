import os
import logging
from flask import Flask
from models.models import db
from routes.upload_routes import upload_csv_routes
from routes.query_routes import query_routes
from routes.test_routes import test_routes
from dotenv import load_dotenv
from datetime import datetime
from waitress import serve

# Load environment variables from .env file
load_dotenv()

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Set up logging
log_file = datetime.now().strftime("%Y-%m-%d") + ".log"
log_path = os.path.join("logs", log_file)
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(upload_csv_routes)
app.register_blueprint(query_routes)
app.register_blueprint(test_routes)

#Error handling for 404 - Page Not Found
@app.errorhandler(404)
def handle_not_found_error(e):
    message = "404 - Page Not Found: " + str(e)
    logging.error(message)
    return message, 404

# Error handling for 500 - Internal Server Error
@app.errorhandler(500)
def handle_internal_server_error(e):
    message = "500 - Internal Server Error: " + str(e)
    logging.error(message)
    return message, 500

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)



