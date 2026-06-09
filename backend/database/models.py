from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ImageAnalysis(Base):

    __tablename__ = "image_analysis"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    camera = Column(String)

    software = Column(String)

    risk = Column(String)

    score = Column(Integer)

    confidence = Column(Float)

    mean_ela = Column(Float)

    std_ela = Column(Float)

    image_path = Column(String)

    ela_path = Column(String)