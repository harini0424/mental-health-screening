import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

load_dotenv()  # reads values from .env file

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class ScreeningResult(Base):
    __tablename__ = "screening_results"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    phq9_score = Column(Integer)
    phq9_severity = Column(String)
    gad7_score = Column(Integer)
    gad7_severity = Column(String)
    self_harm_flag = Column(Boolean)
    emotion_risk_signal = Column(String)
    final_risk_tier = Column(String)
    recommended_action = Column(String)


# Creates the table in the database if it doesn't already exist
def init_db():
    Base.metadata.create_all(bind=engine)