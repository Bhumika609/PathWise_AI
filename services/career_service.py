# services/career_service.py

import re

# Known skills (MVP controlled vocabulary)
KNOWN_SKILLS = {
    "python", "sql", "excel", "statistics",
    "java", "data structures", "algorithms",
    "seo", "social media", "content writing",
    "analytics", "basic math"
}

CAREERS = {
    "Data Analyst": {
        "required_skills": {"excel", "sql", "python", "statistics"}
    },
    "Software Developer": {
        "required_skills": {"python", "java", "data structures", "algorithms"}
    },
    "Digital Marketing Executive": {
        "required_skills": {"seo", "social media", "content writing", "analytics"}
    }
}

# ---------- STEP A: Extract skills mentioned in text ----------
def _extract_skills_from_text(text: str):
    text_lower = text.lower()
    detected = set()

    for skill in KNOWN_SKILLS:
        if skill in text_lower:
            detected.add(skill)

    return detected


# ---------- Infer basic skills from degree ----------
def _infer_user_skills(profile):
    skills = set()

    degree = profile.get("degree")

    if degree == "BSC":
        skills.update({"statistics", "excel"})
    if degree == "BTECH":
        skills.update({"python", "data structures"})
    if degree == "INTERMEDIATE":
        skills.update({"basic math"})
    if degree == "DIPLOMA":
        skills.update({"basic math"})

    return skills


# ---------- STEP B: Generate roadmap ----------
def _generate_roadmap(career_name, missing_skills):
    roadmap = []

    for skill in missing_skills:
        roadmap.append({
            "skill": skill,
            "action": f"Learn {skill} through structured online course and practice projects."
        })

    return {
        "target_career": career_name,
        "steps": roadmap
    }


def get_career_recommendations(profile, text):
    inferred_skills = _infer_user_skills(profile)
    mentioned_skills = _extract_skills_from_text(text)

    # Merge both
    user_skills = inferred_skills.union(mentioned_skills)

    results = []

    for career_name, data in CAREERS.items():
        required = data["required_skills"]
        matched = user_skills.intersection(required)
        missing = required - user_skills

        match_percentage = round((len(matched) / len(required)) * 100, 2)

        roadmap = _generate_roadmap(career_name, missing)

        results.append({
            "career": career_name,
            "match_percentage": match_percentage,
            "matched_skills": list(matched),
            "missing_skills": list(missing),
            "roadmap": roadmap
        })

    results.sort(key=lambda x: x["match_percentage"], reverse=True)

    return results
