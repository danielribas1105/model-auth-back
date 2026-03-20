from fastapi import FastAPI
from app.modules.user.route import router as user_router

app = FastAPI(
    title="Workout Plan API",
    description="API para gerenciamento de planos de treino",
    version="1.0.0",
)

# Registra todos os routers
app.include_router(user_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}
