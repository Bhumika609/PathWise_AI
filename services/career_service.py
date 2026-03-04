# services/career_service.py

KNOWN_SKILLS = {
    "python", "sql", "excel", "statistics",
    "java", "data structures", "algorithms",
    "seo", "social media", "content writing",
    "analytics", "basic math", "communication",
    "problem solving"
}

CAREERS = {
    "Data Analyst": {
        "skills": {"excel": 1, "statistics": 2, "sql": 2, "python": 2},
        "market_demand": "high",
        "preferred_degrees": {"BSC", "BTECH"},
        "duration_months_to_entry": 6
    },
    "Software Developer": {
        "skills": {"python": 2, "java": 2, "data structures": 2, "algorithms": 2},
        "market_demand": "high",
        "preferred_degrees": {"BTECH", "DIPLOMA"},
        "duration_months_to_entry": 12
    },
    "Digital Marketing Executive": {
        "skills": {"seo": 2, "social media": 1, "content writing": 1, "analytics": 2},
        "market_demand": "medium",
        "preferred_degrees": {"BSC", "INTERMEDIATE", "DIPLOMA", "BTECH"},
        "duration_months_to_entry": 4
    }
}

DEMAND_BONUS = {"high": 10, "medium": 5, "low": 0}

SCORING_METHOD = (
    "Feasibility = 0.60*skill_match + 0.25*education_fit + 0.15*constraint_fit + market_bonus"
)

def _extract_skills_from_text(text: str):
    t = (text or "").lower()
    return {s for s in KNOWN_SKILLS if s in t}

def _infer_user_skills(profile: dict):
    degree = profile.get("degree")
    skills = {"communication", "problem solving"}  # baseline

    if degree == "BSC":
        skills.update({"statistics", "excel"})
    elif degree == "BTECH":
        skills.update({"python", "data structures"})
    elif degree == "INTERMEDIATE":
        skills.update({"basic math"})
    elif degree == "DIPLOMA":
        skills.update({"basic math"})

    return skills

def _weighted_skill_match(user_skills: set, career_skills: dict) -> float:
    total = sum(career_skills.values())
    matched = sum(w for s, w in career_skills.items() if s in user_skills)
    return round((matched / total) * 100, 2) if total else 0.0

def _missing_skills(user_skills: set, career_skills: dict):
    return [s for s in career_skills.keys() if s not in user_skills]

def _education_fit(profile: dict, preferred_degrees: set):
    degree = profile.get("degree")
    if not degree:
        return 50.0, "Degree not provided, assuming neutral fit."

    if degree in preferred_degrees:
        return 100.0, f"Degree {degree} matches preferred entry background."

    return 40.0, f"Degree {degree} is not the typical entry path for this role."

def _constraint_fit(text: str, duration_months: int):
    t = (text or "").lower()

    SHORT_PATH_PHRASES = [
    "no long degree",
    "dont want long degree",
    "don't want long degree",
    "short degree",
    "short course",
    "short time",
    "within 6 months",
    "within six months",
    ]

    if any(p in t for p in SHORT_PATH_PHRASES):
        if duration_months <= 6:
            return 100.0, "Matches your preference for shorter pathways."
        return 40.0, "This pathway may take longer than your preference."

    return 70.0, "No strong constraints detected, assuming neutral fit."

def _generate_roadmap(career_name: str, missing_skills: list):
    if not missing_skills:
        return {
            "target_career": career_name,
            "steps": [
                {"step": 1, "action": "Build 2 portfolio projects relevant to the role."},
                {"step": 2, "action": "Create a resume + LinkedIn highlighting projects and skills."},
                {"step": 3, "action": "Apply to internships/entry roles and track weekly."},
            ]
        }

    steps = []
    for i, skill in enumerate(missing_skills, start=1):
        steps.append({
            "step": i,
            "skill": skill,
            "action": f"Learn {skill} using a structured course + practice tasks."
        })

    steps.append({
        "step": len(steps) + 1,
        "action": "Do 1 mini-project combining the learned skills and add it to your portfolio."
    })

    return {"target_career": career_name, "steps": steps}

def _build_feasibility_explanation(demand, skill_score, edu_score, constraint_score, missing):
    bits = [
        f"Market demand: {demand} (bonus {DEMAND_BONUS.get(demand, 0)}).",
        f"Skill match: {skill_score}%.",
        f"Education fit: {edu_score}%.",
        f"Constraint fit: {constraint_score}%."
    ]
    if missing:
        bits.append("Missing skills: " + ", ".join(missing) + ".")
    else:
        bits.append("No missing skills detected.")
    return " ".join(bits)

def get_career_recommendations(profile: dict, text: str):
    inferred = _infer_user_skills(profile)
    mentioned = _extract_skills_from_text(text)
    user_skills = inferred.union(mentioned)

    results = []

    for career_name, meta in CAREERS.items():
        career_skills = meta["skills"]
        demand = meta["market_demand"]
        preferred_degrees = meta["preferred_degrees"]
        duration_months = meta["duration_months_to_entry"]

        skill_score = _weighted_skill_match(user_skills, career_skills)
        missing = _missing_skills(user_skills, career_skills)

        edu_score, edu_reason = _education_fit(profile, preferred_degrees)
        constraint_score, constraint_reason = _constraint_fit(text, duration_months)

        feasibility = (
            0.60 * skill_score +
            0.25 * edu_score +
            0.15 * constraint_score
        )
        feasibility = min(100.0, round(feasibility + DEMAND_BONUS.get(demand, 0), 2))

        roadmap = _generate_roadmap(career_name, missing)
        feasibility_explanation = _build_feasibility_explanation(
            demand, skill_score, edu_score, constraint_score, missing
        )

        results.append({
            "career": career_name,
            "market_demand": demand,
            "match_percentage": skill_score,
            "education_fit": edu_score,
            "constraint_fit": constraint_score,
            "feasibility_score": feasibility,
            "reasoning": {
                "education": edu_reason,
                "constraints": constraint_reason
            },
            "scoring_method": SCORING_METHOD,
            "feasibility_explanation": feasibility_explanation,
            "scoring_method": "Feasibility = 0.60*skill_match + 0.25*education_fit + 0.15*constraint_fit + market_bonus",   
"skill_match_breakdown": {
    "total_weight": sum(career_skills.values()),
    "matched_weight": sum(w for s, w in career_skills.items() if s in user_skills),
    "missing_weight": sum(w for s, w in career_skills.items() if s not in user_skills),
},
"feasibility_explanation": (
    f"Market demand: {demand} (bonus {DEMAND_BONUS.get(demand, 0)}). "
    f"Skill match: {skill_score}%. Education fit: {edu_score}%. Constraint fit: {constraint_score}%. "
    f"Missing skills: {', '.join(missing) if missing else 'none'}."
),    
        "matched_skills": [s for s in career_skills.keys() if s in user_skills],
            "missing_skills": missing,
            "roadmap": roadmap
        })

    results.sort(key=lambda x: x["feasibility_score"], reverse=True)
    return results

def generate_summary(profile: dict, career_matches: list):
    if not career_matches:
        return "No career matches found based on your profile."

    top = career_matches[0]
    career = top["career"]
    feasibility = top["feasibility_score"]
    match = top["match_percentage"]
    missing = top["missing_skills"]

    # IMPORTANT: stop overclaiming
    if feasibility >= 80:
        return (
            f"Best among evaluated options: {career}. High feasibility ({feasibility}%). "
            f"Skill match {match}%. Next: build projects + apply."
        )

    if feasibility >= 50:
        return (
            f"Best among evaluated options: {career}. Moderate feasibility ({feasibility}%). "
            f"Skill match {match}%. Improve by learning: {', '.join(missing)}."
        )

    return (
        f"Best among evaluated options: {career}, but feasibility is low ({feasibility}%). "
        f"Skill match {match}%. Start with: {', '.join(missing)}."
    )
