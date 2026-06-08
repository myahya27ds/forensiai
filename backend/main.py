from fastapi import FastAPI

from backend.database.db import engine
from backend.database.models import Base

from backend.routers.upload import router as upload_router
from backend.routers.history import router as history_router
from backend.routers.report import router as report_router
from backend.routers.delete import router as delete_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ForensiAI",
    version="0.6.0"
)

app.include_router(upload_router)
app.include_router(history_router)
app.include_router(report_router)
app.include_router(delete_router)

@app.get("/")
def root():

    return {
        "message": "ForensiAI Running"
    }