from fastapi import APIRouter

from backend.database.db import SessionLocal
from backend.database.models import ImageAnalysis

router = APIRouter()


@router.get("/history")
def get_history():

    db = SessionLocal()

    try:

        items = db.query(
            ImageAnalysis
        ).all()

        return [
            {
                "id": item.id,
                "filename": item.filename,
                "camera": item.camera,
                "software": item.software,
                "risk": item.risk,
                "score": item.score,
                "confidence": item.confidence,
                "mean_ela": item.mean_ela,
                "std_ela": item.std_ela,
                "image_path": item.image_path,
                "ela_path": item.ela_path,
                "heatmap_path": item.heatmap_path,
                "overlay_path": item.overlay_path
            }
            for item in items
        ]

    finally:

        db.close()