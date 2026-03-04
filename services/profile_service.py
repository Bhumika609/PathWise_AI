# services/profile_service.py
import re
import boto3
import logging
from typing import Optional, Tuple, Dict, Any, List

REGION = "ap-south-1"

logger = logging.getLogger("profile_service")
logger.setLevel(logging.INFO)

comprehend = boto3.client("comprehend", region_name=REGION)

INDIAN_STATES = {
    "andhra pradesh","arunachal pradesh","assam","bihar","chhattisgarh","goa",
    "gujarat","haryana","himachal pradesh","jharkhand","karnataka","kerala",
    "madhya pradesh","maharashtra","manipur","meghalaya","mizoram","nagaland",
    "odisha","punjab","rajasthan","sikkim","tamil nadu","telangana","tripura",
    "uttar pradesh","uttarakhand","west bengal","delhi"
}

def _regex_degree(text: str) -> Optional[str]:
    t = (text or "").lower()
    if "bsc" in t or "b.sc" in t:
        return "BSC"
    if "btech" in t or "b.tech" in t or "engineering" in t:
        return "BTECH"
    if "intermediate" in t or "inter" in t or "12th" in t or "class 12" in t:
        return "INTERMEDIATE"
    if "diploma" in t:
        return "DIPLOMA"
    return None

def _extract_with_comprehend(text: str) -> Tuple[Optional[str], Optional[int]]:
    state = None
    marks = None
    try:
        resp = comprehend.detect_entities(Text=text, LanguageCode="en")
        for ent in resp.get("Entities", []):
            ent_text = (ent.get("Text") or "").strip()
            ent_type = ent.get("Type") or ""

            if ent_type == "LOCATION":
                cand = ent_text.lower()
                if cand in INDIAN_STATES:
                    state = ent_text.title()

            if ent_type == "QUANTITY":
                # only accept if it's clearly percentage-like
                if re.search(r"(%|percent|percentage)\b", ent_text.lower()):
                    m = re.search(r"\b(\d{1,3})\b", ent_text)
                    if m:
                        v = int(m.group(1))
                        if 0 <= v <= 100:
                            marks = v
    except Exception as e:
        logger.warning(f"Comprehend failed: {e}")
    return state, marks

def _parse_marks(text: str) -> Tuple[Optional[int], List[str]]:
    """
    Returns (marks_percent, warnings).
    Handles:
    - 82%, 82 percent
    - 8.2 CGPA/GPA -> 82
    - standalone 82 (ignores 6 months / 2 years etc.)
    """
    t = (text or "").lower()
    warnings: List[str] = []

    # (A) percent patterns: 82%, 82 percent
    m = re.search(r"\b(\d{1,3})\s*(%|percent|percentage)\b", t)
    if m:
        val = int(m.group(1))
        if 0 <= val <= 100:
            return val, warnings
        warnings.append(f"Ignored out-of-range percentage value: {val}.")
        return None, warnings

    # (B) CGPA / GPA patterns: 8.2 cgpa
    if "cgpa" in t or re.search(r"\bgpa\b", t):
        m2 = re.search(r"\b(\d{1,2}(?:\.\d{1,2})?)\s*(cgpa|gpa)\b", t)
        if m2:
            cgpa = float(m2.group(1))
            if 0 < cgpa <= 10:
                pct = int(round((cgpa / 10.0) * 100))
                warnings.append(f"Converted {cgpa} {m2.group(2).upper()} to percentage {pct}.")
                return pct, warnings
            warnings.append(f"Ignored invalid CGPA/GPA value: {cgpa}. Expected 0-10.")
            return None, warnings

    # (C) Fallback: standalone marks 0-100, but IGNORE time units (months/years)
    # Grab all numbers (integers) in text
    nums = [int(x) for x in re.findall(r"\b(\d{1,3})\b", t)]

    if not nums:
        return None, warnings

    # Remove numbers that are part of time expressions: "6 months", "2 years"
    time_nums = set()
    for mm in re.finditer(r"\b(\d{1,3})\s*(month|months|year|years|yr|yrs)\b", t):
        time_nums.add(int(mm.group(1)))

    candidates = [n for n in nums if n not in time_nums and 0 <= n <= 100]

    if candidates:
        # Heuristic: prefer larger candidate (more likely marks than age/small number)
        chosen = max(candidates)
        # If we saw time numbers, call it out (helps demo transparency)
        if time_nums:
            warnings.append(f"Ignored time values {sorted(time_nums)} while extracting marks.")
        return chosen, warnings

    # If only time-like numbers exist or all out of range
    if time_nums:
        warnings.append(f"Found only time-like numbers {sorted(time_nums)}; marks not detected.")
    else:
        warnings.append("No valid marks found (expected percentage 0-100, or CGPA/GPA).")
    return None, warnings

def extract_profile(text: str) -> Dict[str, Any]:
    state_ai, marks_ai = _extract_with_comprehend(text)

    degree = _regex_degree(text)

    marks, warnings = _parse_marks(text)
    # If comprehend gave marks, prefer it (only if sane)
    if marks_ai is not None:
        marks = marks_ai

    profile = {
        "state": state_ai,
        "degree": degree,
        "marks": marks
    }

    # Add extra guardrails
    if profile["marks"] is not None and not (0 <= profile["marks"] <= 100):
        warnings.append(f"Marks out of valid range (0-100): {profile['marks']}. Setting marks=None.")
        profile["marks"] = None

    return {"profile": profile, "warnings": warnings}
