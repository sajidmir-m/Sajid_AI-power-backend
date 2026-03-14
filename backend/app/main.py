from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import Base, engine
from .routes.ingest_routes import router as ingest_router
from .routes.quiz_routes import router as quiz_router
from .routes.answer_routes import router as answer_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Mini Content Ingestion + Adaptive Quiz Engine",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ingest_router)
    app.include_router(quiz_router)
    app.include_router(answer_router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
