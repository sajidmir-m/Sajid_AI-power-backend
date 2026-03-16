from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.inspection import inspect

from .config import settings
from .database import engine
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

    @app.get("/debug/db")
    def debug_db():
        """
        Safe DB debug info: shows host/dbname, table columns, and row counts.
        Does NOT return passwords.
        """
        url = make_url(settings.database_url)
        safe_url = {
            "drivername": url.drivername,
            "host": url.host,
            "port": url.port,
            "database": url.database,
            "username": url.username,
        }

        insp = inspect(engine)
        tables = sorted(insp.get_table_names(schema="public"))

        columns: dict[str, list[dict[str, str]]] = {}
        for t in tables:
            cols = insp.get_columns(t, schema="public")
            columns[t] = [{"name": c["name"], "type": str(c["type"])} for c in cols]

        counts: dict[str, int] = {}
        with engine.connect() as conn:
            for t in tables:
                try:
                    counts[t] = int(conn.execute(text(f'SELECT COUNT(*) FROM public."{t}"')).scalar_one())
                except Exception:
                    counts[t] = -1

        return {"database": safe_url, "tables": tables, "columns": columns, "counts": counts}

    return app


app = create_app()
