from fastapi import APIRouter

from backend.database.db import SessionLocal
from backend.database.models import ImageAnalysis

router = APIRouter()


@router.get("/stats")
def get_stats():

    db = SessionLocal()

    try:

        rows = db.query(
            ImageAnalysis
        ).all()

        total = len(rows)

        low = len([
            x for x in rows
            if x.risk == "LOW"
        ])

        medium = len([
            x for x in rows
            if x.risk == "MEDIUM"
        ])

        high = len([
            x for x in rows
            if x.risk == "HIGH"
        ])

        avg_score = 0
        avg_authenticity = 0
        avg_noise = 0
        avg_ela = 0

        if total > 0:

            avg_score = round(
                sum(
                    x.score
                    for x in rows
                ) / total,
                2
            )

            avg_authenticity = round(
                sum(
                    x.authenticity_score or 0
                    for x in rows
                ) / total,
                2
            )

            avg_noise = round(
                sum(
                    x.mean_noise or 0
                    for x in rows
                ) / total,
                2
            )

            avg_ela = round(
                sum(
                    x.mean_ela or 0
                    for x in rows
                ) / total,
                2
            )

        return {

            "total": total,

            "low": low,

            "medium": medium,

            "high": high,

            "avg_score": avg_score,

            "avg_authenticity":
                avg_authenticity,

            "avg_noise":
                avg_noise,

            "avg_ela":
                avg_ela
        }

    finally:

        db.close()