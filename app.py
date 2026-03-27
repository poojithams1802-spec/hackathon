import pickle
from utils import extract_features

# -------- LOAD MODELS --------
with open("models/deepfake_model.pkl", "rb") as f:
    deepfake_model = pickle.load(f)

with open("models/speaker_model.pkl", "rb") as f:
    speaker_model = pickle.load(f)

# -------- INPUT FILE --------
input_file = "recordings/input.wav"

# -------- FEATURE EXTRACTION --------
features = extract_features(input_file)

# -------- STEP 1: DEEPFAKE CHECK --------
fake_prob = deepfake_model.predict_proba([features])[0][1]

if fake_prob > 0.6:
    print("🚨 RESULT: AI GENERATED VOICE")
    print(f"Fake Confidence: {fake_prob:.2f}")
    exit()

# -------- STEP 2: SPEAKER VERIFICATION --------
speaker_pred = speaker_model.predict([features])[0]
speaker_conf = max(speaker_model.predict_proba([features])[0])

# -------- FINAL DECISION --------
if speaker_pred == 1:
    print("✅ RESULT: AUTHORIZED USER")

else:
    print("⚠️ RESULT: IMPOSTOR (WRONG PERSON)")

# -------- DEBUG INFO --------
print(f"Speaker Confidence: {speaker_conf:.2f}")
print(f"Fake Probability: {fake_prob:.2f}")