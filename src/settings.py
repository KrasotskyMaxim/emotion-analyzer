from dotenv import load_dotenv
import os

load_dotenv()

HOST_URL = os.getenv("HOST_URL", "http://localhost:8000")
STATIC_PATH = os.getenv("STATIC_PATH")
TEMPLATE_PATH = os.getenv("TEMPLATE_PATH", "templates")

DEBUG = bool(os.getenv("DEBUG", False))
