import os

DB_USER = os.getenv("DB_USER", "usuario_hostgator")
DB_PASS = os.getenv("DB_PASS", "senha_hostgator")
DB_NAME = os.getenv("DB_NAME", "brando_db")
DB_HOST = os.getenv("DB_HOST", "mysql.hostgator.com")

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv("SECRET_KEY", "brandoimoveis_secret")
