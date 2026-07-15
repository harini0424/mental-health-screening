# PHQ-9 questions (depression screening)
PHQ9_QUESTIONS = [
    "Little interest or pleasure in doing things",
    "Feeling down, depressed, or hopeless",
    "Trouble falling or staying asleep, or sleeping too much",
    "Feeling tired or having little energy",
    "Poor appetite or overeating",
    "Feeling bad about yourself - or that you are a failure",
    "Trouble concentrating on things",
    "Moving or speaking slowly, or being fidgety/restless",
    "Thoughts that you would be better off dead or of hurting yourself"
]

# GAD-7 questions (anxiety screening)
GAD7_QUESTIONS = [
    "Feeling nervous, anxious, or on edge",
    "Not being able to stop or control worrying",
    "Worrying too much about different things",
    "Trouble relaxing",
    "Being so restless that it's hard to sit still",
    "Becoming easily annoyed or irritable",
    "Feeling afraid as if something awful might happen"
]


def score_phq9(answers):
    """
    answers: list of 9 integers (0-3), one per question
    returns: (total_score, severity_label)
    """
    total = sum(answers)

    if total <= 4:
        severity = "Minimal"
    elif total <= 9:
        severity = "Mild"
    elif total <= 14:
        severity = "Moderate"
    elif total <= 19:
        severity = "Moderately Severe"
    else:
        severity = "Severe"

    return total, severity


def score_gad7(answers):
    """
    answers: list of 7 integers (0-3), one per question
    returns: (total_score, severity_label)
    """
    total = sum(answers)

    if total <= 4:
        severity = "Minimal"
    elif total <= 9:
        severity = "Mild"
    elif total <= 14:
        severity = "Moderate"
    else:
        severity = "Severe"

    return total, severity

def check_self_harm_flag(phq9_answers):
    """
    Checks Question 9 (index 8) of PHQ-9 - the self-harm question.
    Returns True if it needs an urgent flag, regardless of total score.
    """
    question_9_answer = phq9_answers[8]
    return question_9_answer > 0
# Quick test — run this file directly to check it works
if __name__ == "__main__":
    sample_phq9_answers = [2, 1, 3, 2, 1, 0, 1, 0, 2]
    total, severity = score_phq9(sample_phq9_answers)
    urgent_flag = check_self_harm_flag(sample_phq9_answers)
    print(f"PHQ-9 Score: {total} -> {severity}")
    print(f"Urgent flag (self-harm question): {urgent_flag}")

    sample_gad7_answers = [1, 2, 2, 1, 0, 1, 1]
    total, severity = score_gad7(sample_gad7_answers)
    print(f"GAD-7 Score: {total} -> {severity}")