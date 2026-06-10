from backend.database.db import SessionLocal
from backend.database.models import ImageAnalysis

def save_analysis(
    filename,
    metadata,
    analysis,
    ela,
    noise,
    image_path,
    ela_path,
    heatmap_path,
    overlay_path
):

    db = SessionLocal()

    try:

        item = ImageAnalysis(

            filename=filename,

            camera=metadata.get(
                "Model",
                "Unknown"
            ),

            software=metadata.get(
                "Software",
                "Unknown"
            ),

            risk=analysis["risk"],

            score=analysis["score"],

            confidence=analysis.get(
                "confidence",
                None
            ),

            mean_ela=ela["mean_error"],

            std_ela=ela["std_error"],

            noise_level=noise["noise_level"],

            mean_noise=noise["mean_noise"],

            std_noise=noise["std_noise"],

            manipulation_probability=analysis.get("manipulation_probability", None),

            authenticity_score=analysis.get("authenticity_score", None),

            image_path=image_path,

            ela_path=ela_path,

            heatmap_path=heatmap_path,

            overlay_path=overlay_path
        )

        db.add(item)

        db.commit()

    finally:

        db.close()