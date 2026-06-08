from fastapi import APIRouter

from backend.database.db import SessionLocal
from backend.database.models import ImageAnalysis

router = APIRouter()


@router.get("/stats")
def get_stats():

    db = SessionLocal()

    try:

        data = db.query(ImageAnalysis).all()

        total = len(data)

        low = len([
            x for x in data
            if x.risk == "LOW"
        ])

        medium = len([
            x for x in data
            if x.risk == "MEDIUM"
        ])

        high = len([
            x for x in data
            if x.risk == "HIGH"
        ])

        avg_score = 0

        if total > 0:

            avg_score = round(
                sum(x.score for x in data) / total,
                2
            )

        return {
            "total": total,
            "low": low,
            "medium": medium,
            "high": high,
            "avg_score": avg_score
        }

    finally:

        db.close()