import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from utils import extract_features

# ------------------ DEEPFAKE MODEL ------------------
X, y = [], []

for file in os.listdir("data/real"):
    X.append(extract_features("data/real/" + file))
    y.append(0)

for file in os.listdir("data/fake"):
    X.append(extract_features("data/fake/" + file))
    y.append(1)

deepfake_model = RandomForestClassifier()
deepfake_model.fit(X, y)

with open("models/deepfake_model.pkl", "wb") as f:
    pickle.dump(deepfake_model, f)


# ------------------ SPEAKER MODEL ------------------
X_s, y_s = [], []

# USER = 1
for file in os.listdir("data/user"):
    X_s.append(extract_features("data/user/" + file))
    y_s.append(1)

# OTHERS = 0
for file in os.listdir("data/others"):
    X_s.append(extract_features("data/others/" + file))
    y_s.append(0)

speaker_model = RandomForestClassifier()
speaker_model.fit(X_s, y_s)

with open("models/speaker_model.pkl", "wb") as f:
    pickle.dump(speaker_model, f)

print("✅ Models trained and saved!")