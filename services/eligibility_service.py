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

        # ---- State Check ----
        if scheme["state"]:
            if profile["state"] is None:
                eligible = False
                reasons.append("State not provided")
            elif profile["state"] != scheme["state"]:
                eligible = False
                reasons.append("State mismatch")

        # ---- Marks Check ----
        if profile["marks"] is None:
            eligible = False
            reasons.append("Marks not provided")
        elif profile["marks"] < scheme["min_marks"]:
            eligible = False
            reasons.append("Marks below requirement")

        if eligible:
            reasons = ["All criteria satisfied"]

        results.append({
            "scheme": scheme["name"],
            "eligible": eligible,
            "reasons": reasons
        })

    return results
