import pickle
from utils import extract_features
import whisper

# -------- LOAD MODELS --------
with open("models/deepfake_model.pkl", "rb") as f:
    deepfake_model = pickle.load(f)

with open("models/speaker_model.pkl", "rb") as f:
    speaker_model = pickle.load(f)

# -------- LOAD WHISPER --------
whisper_model = whisper.load_model("base")

# -------- INPUT FILE --------
input_file = "recordings/input.wav"

# -------- FEATURE EXTRACTION --------
features = extract_features(input_file)

# -------- STEP 1: DEEPFAKE CHECK --------
fake_prob = deepfake_model.predict_proba([features])[0][1]

if fake_prob > 0.5:
    print("🚨 RESULT: AI GENERATED VOICE")
    print(f"Fake Confidence: {fake_prob:.2f}")
    exit()

# -------- STEP 2: SPEAKER VERIFICATION --------
speaker_pred = speaker_model.predict([features])[0]
speaker_conf = max(speaker_model.predict_proba([features])[0])

# -------- STEP 3: PASSWORD CHECK --------
result = whisper_model.transcribe(input_file)
text = result["text"].lower()

password = "open sesame"

password_ok = password in text

# -------- FINAL DECISION --------
if speaker_pred == 1 and password_ok:
    print("✅ RESULT: AUTHORIZED USER")

elif speaker_pred == 0:
    print("⚠️ RESULT: IMPOSTOR (WRONG PERSON)")

elif not password_ok:
    print("❌ RESULT: WRONG PASSWORD")

else:
    print("❌ RESULT: ACCESS DENIED")

# -------- DEBUG INFO (SHOW THIS IN DEMO) --------
print(f"Speaker Confidence: {speaker_conf:.2f}")
print(f"Fake Probability: {fake_prob:.2f}")
print(f"Recognized Text: {text}")