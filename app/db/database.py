from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Cria o engine de conexão com o PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# Fábrica de sessões — cada requisição abre e fecha uma sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para todos os models
Base = declarative_base()


def get_db():
    """
    Dependency que fornece uma sessão de banco por requisição.
    O 'finally' garante que a sessão sempre será fechada.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
