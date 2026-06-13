from backend.database.db import SessionLocal
from backend.database.models import ImageAnalysis

import json


def save_analysis(
    filename,
    metadata,
    analysis,
    ela,
    noise,
    copymove,
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
            # Copy-Move Analysis
            # =====================

            copymove_detected=int(
                copymove.get(
                    "copymove_detected",
                    False
                )
            ),

            matched_regions=copymove.get(
                "matched_regions",
                0
            ),

            copymove_score=copymove.get(
                "copymove_score",
                0
            ),

            copymove_path=copymove.get(
                "copymove_path",
                None
            ),
            
            clusters=copymove.get(
                "clusters",
                0
            ),

            bbox_count=copymove.get(
                "bbox_count",
                0
            ),

            bbox_path=copymove.get(
                "bbox_path",
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