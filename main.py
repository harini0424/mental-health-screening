from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

from questionnaire import score_phq9, score_gad7, check_self_harm_flag
from emotion_analysis import get_risk_signal
from database import SessionLocal, ScreeningResult, init_db

app = FastAPI(title="Mental Health Screening API")

init_db()  # ensures the table exists when the app starts

# Serve the frontend static files
app.mount("/static", StaticFiles(directory="static"), name="static")


class ScreeningRequest(BaseModel):
    phq9_answers: List[int]       # 9 integers, 0-3 each
    gad7_answers: List[int]       # 7 integers, 0-3 each
    free_text: Optional[str] = "" # optional free-text description


class ScreeningResponse(BaseModel):
    phq9_score: int
    phq9_severity: str
    gad7_score: int
    gad7_severity: str
    self_harm_flag: bool
    emotion_risk_signal: str
    final_risk_tier: str
    recommended_action: str


@app.get("/")
def root():
    return {"message": "Mental Health Screening API is running"}


@app.get("/app")
def serve_frontend():
    return FileResponse("static/index.html")


@app.post("/screen", response_model=ScreeningResponse)
def screen(request: ScreeningRequest):
    # Input validation
    if len(request.phq9_answers) != 9:
        raise ValueError("phq9_answers must contain exactly 9 values")
    if len(request.gad7_answers) != 7:
        raise ValueError("gad7_answers must contain exactly 7 values")

    phq9_total, phq9_severity = score_phq9(request.phq9_answers)
    gad7_total, gad7_severity = score_gad7(request.gad7_answers)
    self_harm = check_self_harm_flag(request.phq9_answers)
    emotion_risk = get_risk_signal(request.free_text)

    # Determine final risk tier and action
    if self_harm:
        final_tier = "urgent"
        action = "Immediate escalation: show crisis helpline info, notify counselor for same-day review."
    elif phq9_severity in ["Severe", "Moderately Severe"] or gad7_severity == "Severe":
        final_tier = "high"
        action = "Recommend booking a counselor session as soon as possible."
    elif phq9_severity == "Moderate" or gad7_severity == "Moderate" or emotion_risk == "high_concern":
        final_tier = "moderate"
        action = "Suggest booking a counselor session; provide self-help resources."
    else:
        final_tier = "low"
        action = "Provide self-help resources and general wellness tips."

    # Save to database
    db = SessionLocal()
    db_record = ScreeningResult(
        phq9_score=phq9_total,
        phq9_severity=phq9_severity,
        gad7_score=gad7_total,
        gad7_severity=gad7_severity,
        self_harm_flag=self_harm,
        emotion_risk_signal=emotion_risk,
        final_risk_tier=final_tier,
        recommended_action=action
    )
    db.add(db_record)
    db.commit()
    db.close()

    return ScreeningResponse(
        phq9_score=phq9_total,
        phq9_severity=phq9_severity,
        gad7_score=gad7_total,
        gad7_severity=gad7_severity,
        self_harm_flag=self_harm,
        emotion_risk_signal=emotion_risk,
        final_risk_tier=final_tier,
        recommended_action=action
    )