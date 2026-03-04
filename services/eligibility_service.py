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

        state_required = scheme["state"]
        user_state = profile.get("state")

        marks_required = scheme["min_marks"]
        user_marks = profile.get("marks")

        # ---- STATE CHECK ----
        if state_required:

            if user_state is None:
                eligible = False
                reasons.append("State not provided")

            elif user_state != state_required:
                eligible = False
                reasons.append("State mismatch")

        # ---- MARKS CHECK ----
        if user_marks is None:
            eligible = False
            reasons.append("Marks not provided")

        elif user_marks < marks_required:
            eligible = False
            reasons.append("Marks below requirement")

        if eligible:
            reasons = ["All criteria satisfied"]

        results.append({
            "scheme": scheme["name"],
            "eligible": eligible,
            "reasons": reasons,
            "criteria_checked": {
                "state": {
                    "required": state_required,
                    "user": user_state,
                    "checked": state_required is not None,
                    "passed": None if state_required is None else user_state == state_required
                },
                "min_marks": {
                    "required": marks_required,
                    "user": user_marks,
                    "checked": True,
                    "passed": None if user_marks is None else user_marks >= marks_required
                }
            }
        })

    return results
