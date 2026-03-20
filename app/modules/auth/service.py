from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

# Contexto de hash — usa bcrypt por padrão
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_senha(senha: str) -> str:
    """Transforma a senha em hash seguro para armazenar no banco."""
    return pwd_context.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Compara senha digitada com o hash armazenado."""
    return pwd_context.verify(senha_plana, senha_hash)


def criar_token(dados: dict) -> str:
    """Gera um JWT com os dados fornecidos e tempo de expiração."""
    payload = dados.copy()
    expira = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expira})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decodificar_token(token: str) -> dict:
    """Decodifica e valida um JWT. Lança exceção se inválido."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise ValueError("Token inválido ou expirado")
