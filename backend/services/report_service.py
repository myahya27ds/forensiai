from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet

import os


def generate_report(data, output_path):

    doc = SimpleDocTemplate(output_path)

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

    # =====================
    # TEXT INFORMATION
    # =====================

    text_fields = [

        "Filename",
        "Camera",
        "Software",
        "Risk",
        "Score",
        "Confidence",
        "Mean ELA",
        "Std ELA"

    ]

    for field in text_fields:

        if field in data:

            content.append(
                Paragraph(
                    f"<b>{field}</b>: {data[field]}",
                    styles["Normal"]
                )
            )

    content.append(
        Spacer(1, 20)
    )

    # =====================
    # ORIGINAL IMAGE
    # =====================

    if (
        "image_path" in data
        and os.path.exists(data["image_path"])
    ):

        content.append(
            Paragraph(
                "Original Image",
                styles["Heading2"]
            )
        )

        content.append(
            Image(
                data["image_path"],
                width=250,
                height=180
            )
        )

        content.append(
            Spacer(1, 15)
        )

    # =====================
    # ELA IMAGE
    # =====================

    if (
        "ela_path" in data
        and os.path.exists(data["ela_path"])
    ):

        content.append(
            Paragraph(
                "ELA Analysis",
                styles["Heading2"]
            )
        )

        content.append(
            Image(
                data["ela_path"],
                width=250,
                height=180
            )
        )

        content.append(
            Spacer(1, 15)
        )

    # =====================
    # HEATMAP
    # =====================

    if (
        "heatmap_path" in data
        and os.path.exists(data["heatmap_path"])
    ):

        content.append(
            Paragraph(
                "Heatmap Analysis",
                styles["Heading2"]
            )
        )

        content.append(
            Image(
                data["heatmap_path"],
                width=250,
                height=180
            )
        )

        content.append(
            Spacer(1, 15)
        )

    # =====================
    # OVERLAY
    # =====================

    if (
        "overlay_path" in data
        and os.path.exists(data["overlay_path"])
    ):

        content.append(
            Paragraph(
                "Overlay Visualization",
                styles["Heading2"]
            )
        )

        content.append(
            Image(
                data["overlay_path"],
                width=250,
                height=180
            )
        )

    doc.build(content)

    return output_path