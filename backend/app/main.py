from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db, SessionLocal
from app.routes.api import router as api_router
from app.seed import seed_all
import logging

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# App
app = FastAPI(
    title="Document Automation System",
    description="Sistema de geração de documentos personalizados",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(api_router)


# Startup
@app.on_event("startup")
async def startup():
    logger.info("Iniciando aplicação...")
    init_db()
    logger.info("Banco de dados inicializado")

    # Criar usuário padrão e templates
    db = SessionLocal()
    try:
        seed_all(db)
    finally:
        db.close()


# Root
@app.get("/")
async def root():
    return {
        "message": "Document Automation API",
        "version": "1.0.0",
        "docs": "/docs"
    }
