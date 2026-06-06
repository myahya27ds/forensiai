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

    # Simpan file upload
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Ambil metadata
    metadata = extract_metadata(file_path)

    # Hitung risiko
    risk_result = calculate_risk(metadata)
    
    # Generate ELA image
    ela_output = (
        UPLOAD_DIR /
        f"ela_{file.filename}"
    )

    ela_result = generate_ela(
    str(file_path),
    str(ela_output)
)
    # Simpan hasil analisis ke database
    save_analysis(
        file.filename,
        metadata,
        risk_result,
        ela_result
    )
    
    return {
        "filename": file.filename,
        "metadata": metadata,
        "analysis": risk_result,
        "ela": ela_result
    }