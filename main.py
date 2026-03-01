from services.career_service import get_career_recommendations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from services.profile_service import extract_profile
from services.eligibility_service import check_eligibility
import logging
from services.career_service import get_career_recommendations

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
    profile = extract_profile(request.text)
    eligibility = check_eligibility(profile)
    career_matches = get_career_recommendations(profile,request.text)

    return {
        "profile": profile,
        "eligibility": eligibility,
        "career_matches": career_matches
    }
