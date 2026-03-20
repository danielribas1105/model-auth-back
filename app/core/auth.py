from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import bcrypt
from app.config import settings


def hash_senha(senha: str) -> str:
    senha_bytes = senha.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha_bytes, salt).decode("utf-8")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha_plana.encode("utf-8"), senha_hash.encode("utf-8"))


def criar_token(dados: dict) -> str:
    payload = dados.copy()
    expira = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload.update({"exp": expira})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decodificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise ValueError("Token inválido ou expirado")
