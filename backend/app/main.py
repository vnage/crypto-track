from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import API_PREFIX
from .routers import portfolio, settings
from .database import engine, Base

# создаем таблицы бд при старте
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Crypto Portfolio Tracker API")

# разрешаем запросы с фронтенда (включая localhost и telegram)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # в продакшене указать конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(portfolio.router, prefix=f"{API_PREFIX}/portfolio", tags=["portfolio"])
app.include_router(settings.router, prefix=f"{API_PREFIX}/settings", tags=["settings"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
