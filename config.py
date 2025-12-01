# =====================================================
#  CONFIGURAÇÃO DE CONEXÃO - BRANDO IMÓVEIS / NOUS
# =====================================================

import os
from urllib.parse import quote_plus

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")

SECRET_KEY = os.getenv("SECRET_KEY", "brandoimoveis_secret")

# 🔑 Senha do painel administrativo
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "@13Lorenzo")

DB_PASS_ENCODED = quote_plus(DB_PASS) if DB_PASS else ""

# URI limpa (sem parâmetros extras)
SQLALCHEMY_DATABASE_URI = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS_ENCODED}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
