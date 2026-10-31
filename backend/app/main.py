from fastapi import FastAPI

app = FastAPI(
    title ="BeloCupCake API",
    description="API do projeto acadêmico BeloCupCake.",
    version="0.1.0",
)

@app.get("/health", tags=["Sistema"])
def verificar_api():
    return {
        "status": "ok",
        "aplicacao:": "BeloCupCake",
    }