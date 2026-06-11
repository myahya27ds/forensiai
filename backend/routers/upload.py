from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

from backend.services.metadata_service import extract_metadata
from backend.services.risk_service import calculate_risk
from backend.services.ela_service import generate_ela
from backend.services.database_service import save_analysis
from backend.services.heatmap_service import generate_heatmap
from backend.services.overlay_service import generate_overlay
from backend.services.image_service import normalize_orientation
from backend.services.noise_service import analyze_noise
from backend.services.explanation_service import generate_explanation

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):

    # =====================
    # Save Upload
    # =====================

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # =====================
    # Normalize Orientation
    # =====================

    normalize_orientation(
        str(file_path)
    )

    # =====================
    # Metadata Extraction
    # =====================

    metadata = extract_metadata(
        str(file_path)
    )

    # =====================
    # ELA Analysis
    # =====================

    ela_output = (
        UPLOAD_DIR /
        f"ela_{file.filename}"
    )

    ela_result = generate_ela(
        str(file_path),
        str(ela_output)
    )

    # =====================
    # Noise Analysis
    # =====================

    noise_result = analyze_noise(
        str(file_path)
    )

    # =====================
    # Heatmap Generation
    # =====================

    heatmap_output = (
        UPLOAD_DIR /
        f"heatmap_{file.filename}"
    )

    heatmap_path = generate_heatmap(
        str(ela_output),
        str(heatmap_output)
    )

    # =====================
    # Overlay Generation
    # =====================

    overlay_output = (
        UPLOAD_DIR /
        f"overlay_{file.filename}"
    )

    overlay_path = generate_overlay(
        str(file_path),
        str(heatmap_output),
        str(overlay_output)
    )

    # =====================
    # Risk Analysis
    # =====================

    analysis = calculate_risk(
        metadata,
        ela_result,
        noise_result
    )

    # =====================
    # AI Explanation
    # =====================

    explanation = generate_explanation(
        metadata,
        analysis,
        ela_result,
        noise_result
    )

    # =====================
    # Save Database
    # =====================

    save_analysis(
        file.filename,
        metadata,
        analysis,
        ela_result,
        noise_result,
        str(file_path),
        ela_result["ela_path"],
        heatmap_path,
        overlay_path,
        explanation
    )

    # =====================
    # Response
    # =====================

    return {

        "filename": file.filename,

        "metadata": metadata,

        "analysis": analysis,

        "noise": noise_result,

        "explanation": explanation,

        "ela": ela_result,

        "image_path": str(file_path),

        "ela_path": ela_result["ela_path"],

        "heatmap_path": heatmap_path,

        "overlay_path": overlay_path

    }