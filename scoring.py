def score_eligibility(responses):
    score_map = {"Yes": 2, "No": 0}

    eb1_score = sum([
        score_map[responses["pub"]],
        score_map[responses["media"]],
        score_map[responses["judge"]],
        score_map[responses["salary"]],
        score_map[responses["contrib"]],
    ])

    eb2_score = eb1_score + 2 if responses["contrib"] == "Yes" else eb1_score

    return {"EB1-A": min(eb1_score, 10), "EB2-NIW": min(eb2_score, 10)}
