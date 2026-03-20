from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, LoginRequest, Token
from app.services.auth import hash_senha, verificar_senha, criar_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/registro", response_model=UsuarioResponse, status_code=201)
def registrar(dados: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se e-mail já existe
    if db.query(Usuario).filter(Usuario.email == dados.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    usuario = Usuario(
        nome=dados.nome, email=dados.email, senha_hash=hash_senha(dados.senha)
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=Token)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
        )

    token = criar_token({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer"}
