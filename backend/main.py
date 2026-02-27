from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum
from services.profile_service import extract_profile
from services.eligibility_service import check_eligibility

app = FastAPI(title="PathWise AI Backend")

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for analyze endpoint
class AnalyzeRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "PathWise backend running"}

@app.get("/health")
def health():
    return {"status": "API healthy"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    profile = extract_profile(request.text)
    eligibility = check_eligibility(profile)

    return {
        "profile": profile,
        "eligibility": eligibility
    }
# Lambda handler
handler = Mangum(app)