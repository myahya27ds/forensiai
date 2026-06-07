from fastapi import APIRouter

from backend.database.db import SessionLocal
from backend.database.models import ImageAnalysis

router = APIRouter()


@router.get("/history")
def get_history():

    db = SessionLocal()

    try:

        data = db.query(
            ImageAnalysis
        ).all()

        results = []

        for item in data:

            results.append({
                "id": item.id,
                "filename": item.filename,
                "camera": item.camera,
                "risk": item.risk,
                "score": item.score,
                "mean_ela": item.mean_ela,
                "std_ela": item.std_ela,
                "image_path": item.image_path,
                "ela_path": item.ela_path
            })

        return results

    finally:
        db.close()