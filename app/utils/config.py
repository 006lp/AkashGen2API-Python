import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_PREFIX = os.getenv("API_PREFIX", "/")
    API_KEY = os.getenv("API_KEY", "test_key")
    SESSION_TOKEN = os.getenv("SESSION_TOKEN", "")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
