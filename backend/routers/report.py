from fastapi import APIRouter
from fastapi.responses import FileResponse

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet

from backend.database.db import SessionLocal
from backend.database.models import ImageAnalysis

import os

router = APIRouter()


@router.get("/report/{item_id}")
def generate_report(item_id: int):

    db = SessionLocal()

    try:

        item = (
            db.query(ImageAnalysis)
            .filter(ImageAnalysis.id == item_id)
            .first()
        )

        if not item:

            return {
                "error": "Data not found"
            }

        os.makedirs(
            "reports",
            exist_ok=True
        )

        pdf_path = os.path.abspath(
            f"reports/report_{item_id}.pdf"
        )

        doc = SimpleDocTemplate(pdf_path)

        styles = getSampleStyleSheet()

        content = []

        content.append(
            Paragraph(
                "ForensiAI Investigation Report",
                styles["Title"]
            )
        )

        content.append(
            Spacer(1, 20)
        )

        fields = [
            ("Filename", item.filename),
            ("Camera", item.camera),
            ("Software", item.software),
            ("Risk", item.risk),
            ("Score", item.score),
            ("Mean ELA", item.mean_ela),
            ("Std ELA", item.std_ela),
        ]

        for label, value in fields:

            content.append(
                Paragraph(
                    f"<b>{label}</b>: {value}",
                    styles["Normal"]
                )
            )

        content.append(
            Spacer(1, 20)
        )

        # ORIGINAL IMAGE

        if (
            item.image_path
            and os.path.exists(
                item.image_path
            )
        ):

            content.append(
                Paragraph(
                    "Original Image",
                    styles["Heading2"]
                )
            )

            content.append(
                Image(
                    os.path.abspath(
                        item.image_path
                    ),
                    width=250,
                    height=180
                )
            )

            content.append(
                Spacer(1, 10)
            )

        # ELA IMAGE

        if (
            item.ela_path
            and os.path.exists(
                item.ela_path
            )
        ):

            content.append(
                Paragraph(
                    "ELA Result",
                    styles["Heading2"]
                )
            )

            content.append(
                Image(
                    os.path.abspath(
                        item.ela_path
                    ),
                    width=250,
                    height=180
                )
            )

        doc.build(content)

        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"report_{item_id}.pdf"
        )

    except Exception as e:

        print("REPORT ERROR:", str(e))

        return {
            "error": str(e)
        }

    finally:

        db.close()