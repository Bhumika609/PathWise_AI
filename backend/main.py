from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum

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
    return {
        "message": "Analyze endpoint working",
        "input_text": request.text
    }

# Lambda handler
handler = Mangum(app)