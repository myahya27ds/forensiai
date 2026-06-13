from fastapi import APIRouter

from backend.database.db import SessionLocal
from backend.database.models import ImageAnalysis

router = APIRouter()


@router.get("/history")
def get_history():

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

                "id": item.id,

                "filename": item.filename,

                "camera": item.camera,

                "software": item.software,

                "risk": item.risk,

                "score": item.score,

                "confidence": item.confidence,

                "manipulation_probability":
                    item.manipulation_probability,

                "authenticity_score":
                    item.authenticity_score,

                "copymove_detected": item.copymove_detected,

                "matched_regions": item.matched_regions,

                "copymove_score": item.copymove_score,

                "copymove_path": item.copymove_path,
                
                "clusters": item.clusters,

                "bbox_count": item.bbox_count,

                "bbox_path": item.bbox_path,
                
                "mean_ela": item.mean_ela,

                "std_ela": item.std_ela,

                "mean_noise": item.mean_noise,

                "std_noise": item.std_noise,

                "noise_level": item.noise_level,

                "image_path": item.image_path,

                "ela_path": item.ela_path,

                "heatmap_path": item.heatmap_path,

                "overlay_path": item.overlay_path,

                "explanation": item.explanation,

                "findings": item.findings

            })

        return results

    finally:

        db.close()