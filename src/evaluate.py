# src/evaluate.py
import joblib
import argparse
import json
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pandas as pd
import re

# same cleaning as in train.py and predict.py
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " url ", text)
    text = re.sub(r"\d+", " number ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def evaluate(model_path, test_path, output_path):
    # Load model & vectorizer (root-level files)
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")

    # Load test data (tab-separated)
    df = pd.read_csv(test_path, sep="\t", names=["label", "message"])
    df = df.dropna(subset=["message"])  # drop empty rows
    df["message"] = df["message"].astype(str).apply(clean_text)

    X_test = vectorizer.transform(df["message"])
    y_test = df["label"]

    # Predict
    y_pred = model.predict(X_test)

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred).tolist()

    # Save results
    results = {"accuracy": acc, "report": report, "confusion_matrix": cm}
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Evaluation complete. Accuracy: {acc:.4f}. Results saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", default=".", help="Path to model/vectorizer (ignored if root-level)")
    parser.add_argument("--test_path", default="data/SMSSpamCollection.txt")
    parser.add_argument("--output_path", default="eval.json")
    args = parser.parse_args()
    evaluate(args.model_path, args.test_path, args.output_path)
