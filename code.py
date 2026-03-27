import os
import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# -------- FEATURE EXTRACTION --------
def extract_features(file):
    y, sr = librosa.load(file, sr=None)
    
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    
    return mfcc_mean


# -------- LOAD DATA --------
X = []
y = []

# REAL = 0
for file in os.listdir("data/real"):
    path = "data/real/" + file
    features = extract_features(path)
    X.append(features)
    y.append(0)

# FAKE = 1
for file in os.listdir("data/fake"):
    path = "data/fake/" + file
    features = extract_features(path)
    X.append(features)
    y.append(1)


# -------- TRAIN MODEL --------
model = RandomForestClassifier()
model.fit(X, y)


# -------- TEST INPUT --------
input_file = "recordings/input.wav"
features = extract_features(input_file)

prediction = model.predict([features])[0]
confidence = max(model.predict_proba([features])[0])


# -------- OUTPUT --------
if prediction == 0:
    print("✅ REAL VOICE")
else:
    print("🚨 FAKE VOICE")

print(f"Confidence: {confidence:.2f}")
