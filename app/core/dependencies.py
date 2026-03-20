from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.modules.user.model import Usuario
from app.modules.auth.service import decodificar_token

# Diz ao FastAPI onde fica o endpoint de login para pegar o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_auth(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependency injetada em rotas protegidas.
    Valida o JWT e retorna o usuário logado.
    """
    credenciais_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decodificar_token(token)
        usuario_id: int = payload.get("sub")
        if usuario_id is None:
            raise credenciais_exception
    except ValueError:
        raise credenciais_exception

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None or not usuario.ativo:
        raise credenciais_exception

    return usuario
