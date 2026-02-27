import re

def extract_profile(text: str):
    profile = {
        "state": None,
        "degree": None,
        "marks": None
    }

    # Extract marks
    marks_match = re.search(r'(\d{2})\s*percent', text.lower())
    if marks_match:
        profile["marks"] = int(marks_match.group(1))

    # Extract state (simple example)
    states = ["karnataka", "tamil nadu", "kerala", "maharashtra"]
    for state in states:
        if state in text.lower():
            profile["state"] = state.title()

    # Extract degree
    degrees = ["bsc", "btech", "ba", "bcom"]
    for degree in degrees:
        if degree in text.lower():
            profile["degree"] = degree.upper()

    return profile