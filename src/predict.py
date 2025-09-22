import joblib
import re

# Load model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

print("Smishing Detection System Ready!")
print("Type a message to test, or 'quit' to exit.\n")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " url ", text)  # replace links
    text = re.sub(r"\d+", " number ", text)  # replace numbers
    text = re.sub(r"[^\w\s]", " ", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()  # remove extra spaces
    return text

while True:
    msg = input("\nEnter a message: ")
    if msg.lower() == "quit":
        break

    # 🔑 Apply same cleaning as training
    msg_clean = clean_text(msg)
    msg_vec = vectorizer.transform([msg_clean])
    prediction = model.predict(msg_vec)[0]

    label = "Smishing/Spam" if prediction == "spam" else "Safe (Ham)"
    print(f" Prediction: {label}")
