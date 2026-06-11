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

        rows = (
            db.query(ImageAnalysis)
            .order_by(
                ImageAnalysis.id.desc()
            )
            .all()
        )

        results = []

        for item in rows:

            results.append({

                # =====================
                # Basic Information
                # =====================

                "id": item.id,

                "filename": item.filename,

                "camera": item.camera,

                "software": item.software,

                # =====================
                # Risk Analysis
                # =====================

                "risk": item.risk,

                "score": item.score,

                "confidence": item.confidence,

                "manipulation_probability":
                    item.manipulation_probability,

                "authenticity_score":
                    item.authenticity_score,

                # =====================
                # ELA Analysis
                # =====================

                "mean_ela": item.mean_ela,

                "std_ela": item.std_ela,

                # =====================
                # Noise Analysis
                # =====================

                "mean_noise": item.mean_noise,

                "std_noise": item.std_noise,

                "noise_level": item.noise_level,

                # =====================
                # AI Investigation
                # =====================

                "explanation": item.explanation,

                "findings": item.findings,

                # =====================
                # Image Paths
                # =====================

                "image_path": item.image_path,

                "ela_path": item.ela_path,

                "heatmap_path": item.heatmap_path,

                "overlay_path": item.overlay_path

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
            index=False,
            encoding="utf-8-sig"
        )

        return FileResponse(
            csv_path,
            media_type="text/csv",
            filename="forensiai_export.csv"
        )

    finally:

        db.close()