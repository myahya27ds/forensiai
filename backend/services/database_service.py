from backend.database.db import SessionLocal
from backend.database.models import ImageAnalysis

import json


def save_analysis(
    filename,
    metadata,
    analysis,
    ela,
    noise,
    image_path,
    ela_path,
    heatmap_path,
    overlay_path,
    explanation=None
):

    db = SessionLocal()

    try:

        item = ImageAnalysis(

            # =====================
            # Basic Info
            # =====================

            filename=filename,

            camera=metadata.get(
                "Model",
                "Unknown"
            ),

            software=metadata.get(
                "Software",
                "Unknown"
            ),

            # =====================
            # Risk Analysis
            # =====================

            risk=analysis["risk"],

            score=analysis["score"],

            confidence=analysis.get(
                "confidence",
                None
            ),

            manipulation_probability=analysis.get(
                "manipulation_probability",
                None
            ),

            authenticity_score=analysis.get(
                "authenticity_score",
                None
            ),

            # =====================
            # ELA Analysis
            # =====================

            mean_ela=ela["mean_error"],

            std_ela=ela["std_error"],

            # =====================
            # Noise Analysis
            # =====================

            mean_noise=noise.get(
                "mean_noise",
                None
            ),

            std_noise=noise.get(
                "std_noise",
                None
            ),

            noise_level=noise.get(
                "noise_level",
                None
            ),

            # =====================
            # AI Explanation
            # =====================

            explanation=explanation,

            findings=json.dumps(
                analysis.get(
                    "findings",
                    []
                )
            ),

            # =====================
            # Image Paths
            # =====================

            image_path=image_path,

            ela_path=ela_path,

            heatmap_path=heatmap_path,

            overlay_path=overlay_path
        )

        db.add(item)

        db.commit()

        db.refresh(item)

        return item.id

    except Exception as e:

        db.rollback()

        print(
            "DATABASE ERROR:",
            str(e)
        )

        raise e

    finally:

        db.close()