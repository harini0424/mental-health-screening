import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

# Load the dataset
df = pd.read_csv("chatbot_data.csv")

print(f"Loaded {len(df)} examples across {df['intent'].nunique()} intents")
print(df['intent'].value_counts())

# Split into train/test sets (to check how well it performs on unseen examples)
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['intent'], test_size=0.2, random_state=42, stratify=df['intent']
)

# Convert text into numerical features using TF-IDF
vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train a simple, fast, explainable classifier
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# Evaluate accuracy on the held-out test examples
y_pred = model.predict(X_test_vec)
print("\nModel performance on test set:")
print(classification_report(y_test, y_pred))

# Save both the trained model and the vectorizer for later use
with open("chatbot_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("chatbot_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("\nModel and vectorizer saved successfully.")