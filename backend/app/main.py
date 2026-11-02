from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import engine
from app.routers.usuarios import router as usuarios_router
from app.routers.autenticacao import router as autenticacao_router
from app.routers.administracao import router as administracao_router
from app.routers.produtos import router as produtos_router
from app.routers.regioes import router as regioes_router


app = FastAPI(
    title="BeloCupCake API",
    description="API do projeto acadêmico BeloCupCake.",
    version="0.1.0",
)

app.include_router(usuarios_router)
app.include_router(autenticacao_router)
app.include_router(administracao_router)
app.include_router(produtos_router)
app.include_router(regioes_router)

@app.get("/health", tags=["Sistema"])
def verificar_api():
    return {
        "status": "ok",
        "aplicacao": "BeloCupCake",
    }


@app.get("/health/db", tags=["Sistema"])
def verificar_banco():
    try:
        with engine.connect() as conexao:
            conexao.execute(text("SELECT 1")).scalar_one()

    except SQLAlchemyError as erro:
        print(
            "Falha na verificação do banco:",
            type(erro).__name__,
        )

        raise HTTPException(
            status_code=503,
            detail="Banco de dados indisponível.",
        ) from erro

    return {
        "status": "ok",
        "banco": "conectado",
    }