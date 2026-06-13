from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ImageAnalysis(Base):

    __tablename__ = "image_analysis"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================
    # Basic Information
    # =====================

    filename = Column(String)

    camera = Column(String)

    software = Column(String)

    # =====================
    # Risk Analysis
    # =====================

    risk = Column(String)

    score = Column(Integer)

    confidence = Column(Float)

    manipulation_probability = Column(Float)

    authenticity_score = Column(Float)

    # =====================
    # ELA Analysis
    # =====================

    mean_ela = Column(Float)

    std_ela = Column(Float)

    # =====================
    # Noise Analysis
    # =====================

    mean_noise = Column(Float)

    std_noise = Column(Float)

    noise_level = Column(String)

    # =====================
    # Copy-Move Analysis
    # =====================

    copymove_detected = Column(Integer)

    matched_regions = Column(Integer)

    copymove_score = Column(Float)

    copymove_path = Column(String)

    clusters = Column(Integer)

    # =====================
    # Clone Localization
    # =====================

    bbox_count = Column(Integer)

    bbox_path = Column(String)

    # =====================
    # AI Explanation
    # =====================

    explanation = Column(String)

    findings = Column(String)

    # =====================
    # Images
    # =====================

    image_path = Column(String)

    ela_path = Column(String)

    heatmap_path = Column(String)

    overlay_path = Column(String)

    