from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

print("DATABASE:", os.path.abspath("forensiai.db"))

DATABASE_URL = "sqlite:///forensiai.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)