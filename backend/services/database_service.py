from backend.database.db import SessionLocal
from backend.database.models import ImageAnalysis


def save_analysis(
    filename,
    metadata,
    analysis,
    ela,
    image_path,
    ela_path
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

            mean_ela=ela["mean_error"],

            std_ela=ela["std_error"],

            image_path=image_path,

            ela_path=ela_path
        )

        db.add(item)

        db.commit()

    finally:
        db.close()