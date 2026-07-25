import pickle
import re

# Load the trained model and vectorizer
with open("chatbot_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("chatbot_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Hard safety net: these keywords ALWAYS trigger crisis response,
# regardless of what the ML model predicts
CRISIS_KEYWORDS = [
    "kill myself", "suicide", "end my life", "hurt myself", "want to die",
    "ending it all", "not want to live", "no reason to live", "self harm",
    "self-harm", "cutting myself", "want to disappear", "better off dead",
    "cant go on", "can't go on", "give up on life"
]

RESPONSES = {
    "score_meaning": "Your PHQ-9 and GAD-7 scores map to a severity band (minimal, mild, moderate, severe) based on validated clinical rubrics. Higher scores suggest more significant symptoms, but this is a screening tool, not a diagnosis.",
    "counselor_booking": "We recommend reaching out to a licensed mental health professional in your area, or your institution's counseling services if available.",
    "crisis": "It sounds like you're going through something really difficult right now. Please reach out immediately: India — iCall: 9152987821 (Mon-Sat, 8am-10pm), AASRA: 9820466726 (24x7). If you're in immediate danger, please contact your local emergency number. You are not alone.",
    "general_resources": "I'm sorry you're going through this. Some general tips: maintain a consistent sleep schedule, stay physically active, keep in touch with people you trust, and consider mindfulness or breathing exercises during stressful moments. If these feelings persist, please consider reaching out to a counselor — you don't have to handle this alone.",
    "about_tool": "This tool provides a screening based on standardized clinical questionnaires (PHQ-9, GAD-7) combined with NLP-based emotion analysis. It is not a diagnosis — please consult a licensed professional for a full evaluation. Your data is stored securely.",
    "greeting": "Hello! I'm here to help answer questions about your screening, mental health resources, or how to get support. What would you like to know?",
    "fallback": "I'm not able to answer that specific question, but I can help with understanding your score, finding a counselor, or general self-care resources. If you're in crisis, please reach out to a helpline immediately."
}


def get_chatbot_response(user_message: str) -> dict:
    message_lower = user_message.lower()

    # SAFETY NET FIRST — always checked before the ML model
    for keyword in CRISIS_KEYWORDS:
        if keyword in message_lower:
            return {
                "intent": "crisis",
                "response": RESPONSES["crisis"],
                "matched_by": "keyword_safety_net"
            }

    # ML-based intent classification
    vec = vectorizer.transform([user_message])
    predicted_intent = model.predict(vec)[0]

    # Get confidence score
    probabilities = model.predict_proba(vec)[0]
    confidence = max(probabilities)

    # Low confidence -> fallback response instead of guessing
    if confidence < 0.25:
        return {
            "intent": "fallback",
            "response": RESPONSES["fallback"],
            "matched_by": "low_confidence_fallback"
        }

    return {
        "intent": predicted_intent,
        "response": RESPONSES.get(predicted_intent, RESPONSES["fallback"]),
        "matched_by": "ml_classifier"
    }