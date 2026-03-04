from fastapi import FastAPI, UploadFile, File, HTTPException
# ... keep your existing imports

from services.s3_service import upload_bytes_to_s3
from services.transcribe_service import start_transcription_job, wait_for_transcription, fetch_transcript_text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging

from services.profile_service import extract_profile
from services.eligibility_service import check_eligibility
from services.career_service import get_career_recommendations, generate_summary

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PathWise AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=5)

@app.get("/")
def home():
    return {"message": "PathWise backend running on AWS 🚀"}

@app.get("/health")
def health():
    return {"status": "API healthy"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    text = request.text

    profile_result = extract_profile(text)         # <-- now returns {"profile":..., "warnings":[...]}
    profile = profile_result["profile"]
    warnings = profile_result.get("warnings", [])

    eligibility = check_eligibility(profile)
    career_matches = get_career_recommendations(profile, text)
    summary = generate_summary(profile, career_matches)

    logger.info(f"Received text: {text}")
    logger.info(f"Extracted profile: {profile}")
    logger.info(f"Warnings: {warnings}")
    logger.info(f"Eligibility result: {eligibility}")
    logger.info(f"Career top match: {career_matches[0] if career_matches else None}")
    logger.info(f"Summary: {summary}")

    return {
        "profile": profile,
        "warnings": warnings,
        "eligibility": eligibility if eligibility is not None else [],
        "career_matches": career_matches,
        "ai_summary": summary,
        "skill_detection_note": "Skills are inferred from degree baseline + keyword detection from user text (MVP heuristic)."
    }
@app.post("/transcribe-analyze")
async def transcribe_analyze(file: UploadFile = File(...)):
    """
    Upload audio -> Transcribe -> run analyze pipeline on transcript.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    # allow only common formats
    allowed = {"mp3", "mp4", "wav", "m4a"}
    ext = (file.filename.split(".")[-1] or "").lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    # 1) upload to S3
    s3_uri = upload_bytes_to_s3(audio_bytes, file.filename, file.content_type or "application/octet-stream")

    # 2) start transcribe
    job_name = start_transcription_job(s3_uri=s3_uri, media_format=ext, language_code="en-IN")

    # 3) wait + fetch transcript
    job_resp = wait_for_transcription(job_name, timeout_seconds=180)
    status = job_resp["TranscriptionJob"]["TranscriptionJobStatus"]

    if status == "FAILED":
        reason = job_resp["TranscriptionJob"].get("FailureReason", "unknown")
        raise HTTPException(status_code=500, detail=f"Transcribe failed: {reason}")

    transcript_uri = job_resp["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    text = fetch_transcript_text(transcript_uri)

    # 4) reuse your existing analyze pipeline
    profile = extract_profile(text)
    eligibility = check_eligibility(profile)
    career_matches = get_career_recommendations(profile, text)
    summary = generate_summary(profile, career_matches)

    return {
        "transcribe": {
            "job_name": job_name,
            "s3_uri": s3_uri,
            "transcript_uri": transcript_uri
        },
        "text": text,
        "profile": profile,
        "warnings": [],
        "eligibility": eligibility if eligibility is not None else [],
        "career_matches": career_matches,
        "ai_summary": summary,
        "skill_detection_note": "Skills are inferred from degree baseline + keyword detection from user text (MVP heuristic)."
    }
