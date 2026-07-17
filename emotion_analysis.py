from transformers import pipeline

# Load the pre-trained emotion detection model
# This downloads the model the first time you run it (a few hundred MB, one-time only)
emotion_classifier = pipeline(
    "text-classification",
    model="./emotion_model",
    top_k=None
)


def analyze_emotion(text):
    """
    text: a string (free-text response from the user)
    returns: list of dicts like [{"label": "sadness", "score": 0.82}, ...]
             sorted by score, highest first
    """
    if not text or not text.strip():
        return []

    results = emotion_classifier(text)[0]  # returns list of {label, score} for all emotions
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def get_risk_signal(text):
    """
    Simplified risk signal based on top emotion.
    Returns a label: 'high_concern', 'moderate_concern', or 'low_concern'
    """
    emotions = analyze_emotion(text)
    if not emotions:
        return "low_concern"

    top_emotion = emotions[0]["label"]
    top_score = emotions[0]["score"]

    high_risk_emotions = ["sadness", "fear"]

    if top_emotion in high_risk_emotions and top_score > 0.6:
        return "high_concern"
    elif top_emotion in high_risk_emotions:
        return "moderate_concern"
    else:
        return "low_concern"


# Quick test
if __name__ == "__main__":
    sample_text = "I've been feeling really overwhelmed and hopeless lately. Nothing seems to help."
    emotions = analyze_emotion(sample_text)
    print("Emotion breakdown:")
    for e in emotions:
        print(f"  {e['label']}: {e['score']:.2f}")

    risk = get_risk_signal(sample_text)
    print(f"\nRisk signal: {risk}")