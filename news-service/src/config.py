import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET_AUTH = os.environ.get("SECRET_AUTH")
ALGORITHM = os.environ.get("ALGORITHM")

SECRET_KEY = os.environ.get("SECRET_KEY")

SUPER_USER_EMAIL = os.environ.get("SUPER_USER_EMAIL")
SUPER_USER_PASSWORD = os.environ.get("SUPER_USER_PASSWORD")