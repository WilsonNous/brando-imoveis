import os
from urllib.parse import quote_plus


def required_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variável de ambiente obrigatória ausente: {name}")
    return value


DB_USER = required_env("DB_USER")
DB_PASS = required_env("DB_PASS")
DB_NAME = required_env("DB_NAME")
DB_HOST = required_env("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

SECRET_KEY = required_env("SECRET_KEY")
ADMIN_PASSWORD = required_env("ADMIN_PASSWORD")

DB_PASS_ENCODED = quote_plus(DB_PASS)
DB_USER_ENCODED = quote_plus(DB_USER)
DB_NAME_ENCODED = quote_plus(DB_NAME)

SQLALCHEMY_DATABASE_URI = (
    f"mysql+mysqlconnector://{DB_USER_ENCODED}:{DB_PASS_ENCODED}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME_ENCODED}?charset=utf8mb4"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# O MySQL Connector valida o certificado e o hostname por padrão quando TLS
# está habilitado; o CA do sistema operacional é utilizado para validação.
SQLALCHEMY_ENGINE_OPTIONS = {
    "connect_args": {
        "ssl_disabled": False,
        "ssl_verify_cert": True,
        "ssl_verify_identity": True,
    }
}
