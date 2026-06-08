from fastapi import APIRouter
from fastapi.responses import FileResponse

from backend.database.db import SessionLocal
from backend.database.models import ImageAnalysis

import pandas as pd
import os

router = APIRouter()


@router.get("/export")
def export_csv():

    db = SessionLocal()

    try:

        data = (
            db.query(ImageAnalysis)
            .all()
        )

        results = []

        for item in data:

            results.append({
                "id": item.id,
                "filename": item.filename,
                "camera": item.camera,
                "software": item.software,
                "risk": item.risk,
                "score": item.score,
                "mean_ela": item.mean_ela,
                "std_ela": item.std_ela,
                "image_path": item.image_path,
                "ela_path": item.ela_path
            })

        os.makedirs(
            "exports",
            exist_ok=True
        )

        csv_path = os.path.abspath(
            "exports/forensiai_export.csv"
        )

        df = pd.DataFrame(results)

        df.to_csv(
            csv_path,
            index=False
        )

        return FileResponse(
            csv_path,
            media_type="text/csv",
            filename="forensiai_export.csv"
        )

    finally:

        db.close()