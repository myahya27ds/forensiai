from backend.database.db import SessionLocal
from backend.database.models import ImageAnalysis

def save_analysis(
    filename,
    metadata,
    analysis,
    ela
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

            confidence=analysis["confidence"],

            mean_ela=ela["mean_error"],

            std_ela=ela["std_error"],

            image_path=ela["image_path"],

            ela_path=ela["ela_path"]
        )

        db.add(item)

        db.commit()

    finally:

        db.close()