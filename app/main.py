from fastapi import FastAPI

from app import router


app = FastAPI(
    title="Authentication API",
    description="API template for user authentication",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}


app.include_router(router.router)
