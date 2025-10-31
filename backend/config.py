import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', False)
    API_HOST = os.getenv('API_HOST', '127.0.0.1')
    API_PORT = int(os.getenv('API_PORT', 5000))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Database
    DATABASE_PATH = "data/guardian_db.json"
    DATA_DIR = "data"
    
    # Security
    CORS_ORIGINS = ["*"]  # Restrict in production
    API_TIMEOUT = 30
