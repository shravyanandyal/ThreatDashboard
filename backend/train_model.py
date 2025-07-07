"""import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from sklearn.ensemble import RandomForestClassifier

RandomForestClassifier(n_estimators=150, max_depth=20, random_state=42)


load_dotenv()

# 1) Fetch data from MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
records = list(db[os.getenv("COLLECTION_NAME")].find({}))

df = pd.DataFrame(records)
print("Columns:", df.columns.tolist())
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Ensure no NaN
df = df.dropna(subset=["cleaned_threat_description", "threat_category"])


print("Label distribution:\n", df["threat_category"].value_counts())

# 2) Build pipeline: TF-IDF → Logistic Regression
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 3),
        stop_words="english"
    )),
    ("clf", RandomForestClassifier(
        n_estimators=150,
        max_depth=20,
        random_state=42
    ))
])


# Pre-clean description (optional)
df["cleaned_threat_description"] = df["cleaned_threat_description"].str.lower().str.replace(r"[^a-z\s]", "", regex=True)

# 3) Train
X = df["cleaned_threat_description"]
y = df["threat_category"]
pipeline.fit(X, y)

vectorizer = pipeline.named_steps["tfidf"]
clf = pipeline.named_steps["clf"]

# Get feature names and importances
features = vectorizer.get_feature_names_out()
importances = clf.feature_importances_

# Top 10 important features
top_indices = importances.argsort()[-10:][::-1]
top_features = [(features[i], importances[i]) for i in top_indices]

print("Top 10 important words overall:")
for word, score in top_features:
    print(f"{word}: {score:.4f}")


# 4) Save model
model_path = os.path.join("model", "threat_model.pkl")
os.makedirs("model", exist_ok=True)
with open(model_path, "wb") as f:
    pickle.dump(pipeline, f)

print(f"Model trained on {len(df)} samples and saved to {model_path}")
print("🔍 Prediction Tests:")
print("Phishing →", pipeline.predict(["Fake login page asking for credentials"]))
print("DDoS →", pipeline.predict(["Massive DDoS attack from botnet on port 443"]))
print("Malware →", pipeline.predict(["Detected malicious payload from trojan downloader"]))
print("Ransomware →", pipeline.predict(["Encrypted files and ransom note found on desktop"]))

"""
import os
import pickle
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import ExtraTreesClassifier  # ⬅️ Better than RandomForest

load_dotenv()

# 1. Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

# 2. Load data
records = list(collection.find({}))
df = pd.DataFrame(records)
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# 3. Drop rows missing required fields
df = df.dropna(subset=["threat_category", "cleaned_threat_description"])

# 4. Combine fields for training input
df["text"] = (
    df["threat_actor"].fillna("") + " " +
    df["attack_vector"].fillna("") + " " +
    df["cleaned_threat_description"].fillna("")
)

# 5. Strip extra spaces and fix noisy rows
df["threat_category"] = df["threat_category"].str.strip()
df = df[df["cleaned_threat_description"].str.len() > 30]
df = df[df["text"].str.len() > 50]

# 6. Print class distribution
print("Label distribution:\n", df["threat_category"].value_counts())

# 7. Build training pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=20000,
        ngram_range=(1, 4),       # include up to 4-grams
        stop_words="english",
        min_df=2                  # ignore very rare words
    )),
    ("clf", ExtraTreesClassifier(
        n_estimators=400,
        max_depth=None,
        class_weight='balanced',
        random_state=42
    ))
])

# 8. Train the model
X = df["text"]
y = df["threat_category"]
pipeline.fit(X, y)

# 9. Save the model
os.makedirs("model", exist_ok=True)
model_path = os.path.join("model", "threat_model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(pipeline, f)

print(f"\n✅ Model trained on {len(df)} samples and saved to {model_path}")

# 10. Test predictions
print("\n🔍 Prediction Tests:")
samples = [
    "Fake login page asking for user credentials",
    "DDoS flooding detected on port 443 from botnet IPs",
    "Encrypted files and ransom note left on desktop",
    "Malware dropper executing payload on host system"
]
for s in samples:
    pred = pipeline.predict([s])[0]
    print(f"{s} → {pred}")
