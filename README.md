AI-Powered Voice Authentication System with Deepfake Detection

Problem Statement
With the rapid advancement of AI-generated voice cloning and impersonation attacks, traditional authentication systems such as passwords and OTPs are becoming increasingly vulnerable. There is a need for a secure authentication system that verifies both the speaker’s identity and the correctness of the spoken password, while also detecting synthetic (AI-generated) voices and alerting users of potential threats.

Solution Overview
This project introduces a voice-based authentication system that combines:
- Speaker Verification – Identifies the user based on voice biometrics  
- Voice Password Recognition – Verifies the spoken password  
- Deepfake Detection – Detects AI-generated or manipulated voices  
- Threat Alert System – Sends alerts on suspicious or fake voice attempts

Features
-  Voice-based login system  
-  Speaker identity verification  
-  Spoken password validation  
-  Fake (AI-generated) voice detection  
-  Real-time threat alerts  
-  Confidence score display

Tech Stack

Languages
- Python  
- JavaScript  
- HTML/CSS  

Frameworks & Libraries
- Flask / FastAPI  
- librosa (audio processing)  
- scikit-learn (machine learning)  
- Whisper (speech-to-text)  

System Architecture

1. User records voice input  
2. Audio is processed and features are extracted  
3. Speech is converted to text  
4. System performs:
   - Password validation  
   - Speaker verification  
   - Deepfake detection  
5. Final output:
   -  Access Granted  
   -  Access Denied  
   -  Alert triggered if fake voice detected

Team Members
- Poojitha MS
- Vanditha Pawar
- Kalpana YM
- Varuni Deshpande
