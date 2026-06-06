from fastapi import FastAPI

from backend.database.db import engine
from backend.database.models import Base

from backend.routers.upload import router as upload_router
from backend.routers.history import router as history_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ForensiAI",
    version="0.1.0"
)

app.include_router(upload_router)
app.include_router(history_router)

@app.get("/")
def root():
    return {
        "message": "ForensiAI Running"
    }