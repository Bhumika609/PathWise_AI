def check_eligibility(profile: dict):
    schemes = [
        {
            "name": "Karnataka Merit Scholarship",
            "min_marks": 75,
            "state": "Karnataka"
        },
        {
            "name": "National Skill Grant",
            "min_marks": 60,
            "state": None
        }
    ]

    results = []

    for scheme in schemes:
        eligible = True
        reasons = []

        if scheme["state"] and profile["state"] != scheme["state"]:
            eligible = False
            reasons.append("State mismatch")

        if profile["marks"] and profile["marks"] < scheme["min_marks"]:
            eligible = False
            reasons.append("Marks below requirement")

        results.append({
            "scheme": scheme["name"],
            "eligible": eligible,
            "reasons": reasons if not eligible else ["All criteria satisfied"]
        })

    return results