from fastapi import FastAPI
from starlette.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from .routes import router
from .database.db import Base, engine

app = FastAPI()

# Create DB tables (just for development; later we'll use Alembic)
Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(router)

# Prometheus metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
