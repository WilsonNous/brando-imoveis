# =====================================================
#  CONFIGURAÇÃO DE CONEXÃO - BRANDO IMÓVEIS / NOUS
# =====================================================
# Este arquivo define as variáveis de ambiente e monta
# a URI segura de conexão MySQL para uso no Render.
# Driver: mysql.connector (100% compatível com HostGator)
# =====================================================

import os
from urllib.parse import quote_plus

# -----------------------------------------------------
# Variáveis de ambiente (Render ou .env local)
# -----------------------------------------------------
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
SECRET_KEY = os.getenv("SECRET_KEY", "brandoimoveis_secret")

# -----------------------------------------------------
# Codificação segura da senha (protege caracteres #, @, %, etc)
# -----------------------------------------------------
DB_PASS_ENCODED = quote_plus(DB_PASS) if DB_PASS else ""

# -----------------------------------------------------
# Constrói a URI usando o driver mysqlconnector
# -----------------------------------------------------
SQLALCHEMY_DATABASE_URI = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS_ENCODED}@{DB_HOST}/{DB_NAME}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# -----------------------------------------------------
# Diagnóstico opcional (para logs de inicialização)
# -----------------------------------------------------
def test_database_uri():
    """Exibe a URI de conexão mascarada (para debug controlado)."""
    hidden_pass = "***" if DB_PASS else "(sem senha)"
    print("🔗 Conectando ao banco MySQL (Nous):")
    print(f"   Host: {DB_HOST}")
    print(f"   DB:   {DB_NAME}")
    print(f"   User: {DB_USER}")
    print(f"   Pass: {hidden_pass}")
    print(f"   Driver: mysql.connector\n")

# Executa log ao inicializar (modo debug)
if __name__ == "__main__":
    test_database_uri()
