def score_eligibility(responses):
    score_map = {"Yes": 2, "No": 0}
    return {
        "Publications": score_map[responses["pub"]],
        "Media": score_map[responses["media"]],
        "Judging": score_map[responses["judge"]],
        "Contributions": score_map[responses["contrib"]],
        "Salary": score_map[responses["salary"]],
        "Memberships": score_map[responses["memberships"]],
        "Awards": score_map[responses["awards"]],
        "Display of Work": score_map[responses["display"]],
        "Critical Role": score_map[responses["role"]],
        "Commercial Success": score_map[responses["commercial"]],
    }
