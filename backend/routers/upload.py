from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

from backend.services.metadata_service import extract_metadata
from backend.services.risk_service import calculate_risk
from backend.services.ela_service import generate_ela
from backend.services.database_service import save_analysis

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
    # Metadata
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
    # Risk Analysis
    # =====================

    analysis = calculate_risk(
        metadata,
        ela_result
    )

    # =====================
    # Save Database
    # =====================

    save_analysis(
        file.filename,
        metadata,
        analysis,
        ela_result
    )

    # =====================
    # Response
    # =====================

    return {
        "filename": file.filename,
        "metadata": metadata,
        "analysis": analysis,
        "ela": ela_result,
        "image_path": str(file_path),
        "ela_path": ela_result["ela_path"]
    }