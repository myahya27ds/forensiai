from fastapi import APIRouter

from backend.database.db import SessionLocal
from backend.database.models import ImageAnalysis

router = APIRouter()


@router.delete("/analysis/{item_id}")
def delete_analysis(item_id: int):

    db = SessionLocal()

    try:

        item = (
            db.query(ImageAnalysis)
            .filter(ImageAnalysis.id == item_id)
            .first()
        )

        if not item:

            return {
                "error": "Data not found"
            }

        db.delete(item)

        db.commit()

        return {
            "message": "Analysis deleted"
        }

    finally:

        db.close()