import re
import boto3

REGION = "ap-south-1"
comprehend = boto3.client("comprehend", region_name=REGION)

# Basic known Indian states list (MVP – extend later)
INDIAN_STATES = {
    "andhra pradesh","arunachal pradesh","assam","bihar","chhattisgarh","goa",
    "gujarat","haryana","himachal pradesh","jharkhand","karnataka","kerala",
    "madhya pradesh","maharashtra","manipur","meghalaya","mizoram","nagaland",
    "odisha","punjab","rajasthan","sikkim","tamil nadu","telangana","tripura",
    "uttar pradesh","uttarakhand","west bengal","delhi"
}

def _regex_degree(text: str):
    t = text.lower()
    # MVP mapping
    if "bsc" in t or "b.sc" in t:
        return "BSC"
    if "btech" in t or "b.tech" in t or "engineering" in t:
        return "BTECH"
    if "intermediate" in t or "inter" in t or "12th" in t:
        return "INTERMEDIATE"
    if "diploma" in t:
        return "DIPLOMA"
    return None

def _regex_marks(text: str):
    # Matches: 82, 82%, 82 percent, 82 percentage
    m = re.search(r"\b(\d{1,2})\s*(%|percent|percentage)\b", text.lower())
    if m:
        return int(m.group(1))
    # fallback: any standalone 2-digit number (risky but MVP)
    m2 = re.search(r"\b(\d{1,2})\b", text)
    if m2:
        return int(m2.group(1))
    return None

def _extract_with_comprehend(text: str):
    """
    Returns best-guess (state, marks) using Comprehend entities.
    """
    state = None
    marks = None

    try:
        resp = comprehend.detect_entities(Text=text, LanguageCode="en")
        for ent in resp.get("Entities", []):
            t = ent.get("Text", "")
            ent_type = ent.get("Type", "")

            if ent_type == "LOCATION":
                cand = t.strip().lower()
                if cand in INDIAN_STATES:
                    state = t.strip().title()

            if ent_type == "QUANTITY":
                # looks like "82 percent"
                m = re.search(r"\b(\d{1,2})\b", t)
                if m:
                    marks = int(m.group(1))

    except Exception:
        # Silent fail — we rely on regex fallback
        pass

    return state, marks

def extract_profile(text: str):
    """
    Hybrid extractor:
    - Comprehend for LOCATION/QUANTITY
    - Regex fallback for degree + missing fields
    """
    state_ai, marks_ai = _extract_with_comprehend(text)

    degree = _regex_degree(text)
    marks = marks_ai if marks_ai is not None else _regex_marks(text)
    state = state_ai

    return {
        "state": state,
        "degree": degree,
        "marks": marks
    }
