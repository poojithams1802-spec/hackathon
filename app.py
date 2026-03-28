from flask import Flask, render_template, request, jsonify
import pickle
import os
from utils import extract_features

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['JSON_SORT_KEYS'] = False

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Ensure recordings folder exists
os.makedirs("recordings", exist_ok=True)

# Load models
with open("models/deepfake_model.pkl", "rb") as f:
    deepfake_model = pickle.load(f)

with open("models/speaker_model.pkl", "rb") as f:
    speaker_model = pickle.load(f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/login", methods=["POST"])
def login():
    try:
        if "audio" not in request.files:
            return jsonify({"status": "ERROR", "message": "❌ No audio file uploaded"}), 400

        audio = request.files["audio"]
        user_id = request.form.get("userId", "Unknown")

        if not audio.filename:
            return jsonify({"status": "ERROR", "message": "❌ No file selected"}), 400


        filepath = "recordings/input.wav"
        audio.save(filepath)

        # Extract features
        features = extract_features(filepath)

        # Step 1: Deepfake detection
        fake_prob = deepfake_model.predict_proba([features])[0][1]

        if fake_prob > 0.6:
            return jsonify({
                "status": "AI",
                "message": "🚨 AI GENERATED VOICE",
                "speaker_conf": 0,
                "fake_prob": round(fake_prob, 2)
            })

        # Step 2: Speaker verification
        speaker_pred = speaker_model.predict([features])[0]
        speaker_conf = max(speaker_model.predict_proba([features])[0])

        if speaker_pred == 1:
            status = "AUTHORIZED"
            message = f"✅ AUTHORIZED USER ({user_id})"
        else:
            status = "UNAUTHORIZED"
            message = "⚠️ IMPOSTOR DETECTED"

        return jsonify({
            "status": status,
            "message": message,
            "speaker_conf": round(speaker_conf, 2),
            "fake_prob": round(fake_prob, 2)
        })
    except Exception as e:
        print(f"Error in login: {str(e)}")
        return jsonify({"status": "ERROR", "message": f"❌ Server error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, host='127.0.0.1', port=5050)