import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import resample
import joblib
import re

print(" Training script started")

# Load dataset
df = pd.read_csv(
    "data/SMSSpamCollection.txt",
    sep="\t",
    header=None,
    names=["label", "message"]
)

# Remove NaN
df = df.dropna(subset=["message"])
df["message"] = df["message"].astype(str)

# Text cleaning function
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " url ", text)  # replace links
    text = re.sub(r"\d+", " number ", text)  # replace numbers
    text = re.sub(r"[^\w\s]", " ", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()  # remove extra spaces
    return text

df["message"] = df["message"].apply(clean_text)

print(f" Data loaded: {df.shape[0]} rows")

# Balance dataset (upsample spam)
ham = df[df.label == "ham"]
spam = df[df.label == "spam"]

spam_upsampled = resample(
    spam,
    replace=True,                 # sample with replacement
    n_samples=len(ham),           # match number of ham messages
    random_state=42
)

df_balanced = pd.concat([ham, spam_upsampled])
print(f" Balanced dataset: {df_balanced.label.value_counts().to_dict()}")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    df_balanced["message"], df_balanced["label"], test_size=0.2, random_state=42
)
print(" Data split completed")

# Vectorize with TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train Logistic Regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
acc = accuracy_score(y_test, y_pred)
print(f" Accuracy: {acc:.2f}")
print("\n Classification Report:\n")
print(classification_report(y_test, y_pred))

# Save
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print(" Model & vectorizer saved successfully!")
print(" Training script completed")