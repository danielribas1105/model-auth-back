from fastapi import FastAPI

# Cria a instância principal da aplicação
app = FastAPI(
    title="Meu Backend", description="API construída com FastAPI", version="0.1.0"
)


# Rota GET na raiz "/"
@app.get("/")
def raiz():
    return {"mensagem": "Olá, FastAPI está funcionando!"}


# Rota GET com parâmetro de path
@app.get("/usuarios/{usuario_id}")
def buscar_usuario(usuario_id: int):
    return {"usuario_id": usuario_id, "nome": f"Usuário {usuario_id}"}


# Rota GET com parâmetro de query (?nome=João)
@app.get("/saudacao")
def saudar(nome: str = "visitante"):
    return {"mensagem": f"Olá, {nome}!"}
