let mediaRecorder;
let audioChunks = [];
let recordedBlob = null;

// Recording controls
const recordBtn = document.getElementById('recordBtn');
const stopBtn = document.getElementById('stopBtn');
const playBtn = document.getElementById('playBtn');
const audioPreview = document.getElementById('audioPreview');
const fileInput = document.getElementById('audioFile');

if (recordBtn && stopBtn && playBtn && audioPreview) {
    recordBtn.onclick = async function () {
        audioChunks = [];
        recordedBlob = null;
        playBtn.disabled = true;
        audioPreview.style.display = 'none';
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
            mediaRecorder.onstop = () => {
                recordedBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioPreview.src = URL.createObjectURL(recordedBlob);
                audioPreview.style.display = 'block';
                playBtn.disabled = false;
                // Set the file input to the recorded blob for upload
                const file = new File([recordedBlob], 'recorded.wav', { type: 'audio/wav' });
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                fileInput.files = dataTransfer.files;
            };
            mediaRecorder.start();
            recordBtn.disabled = true;
            stopBtn.disabled = false;
        } catch (err) {
            alert('Microphone access denied or not available.');
        }
    };

    stopBtn.onclick = function () {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            recordBtn.disabled = false;
            stopBtn.disabled = true;
        }
    };

    playBtn.onclick = function () {
        if (audioPreview.src) {
            audioPreview.play();
        }
    };
}

window.uploadAudio = async function () {
    console.log("Login button clicked");


    const userId = document.getElementById("userId").value;

    if (!userId) {
        alert("Enter User ID");
        return;
    }


    if (!fileInput.files.length) {
        alert("Upload or record a .wav file");
        return;
    }

    const formData = new FormData();
    formData.append("audio", fileInput.files[0]);
    formData.append("userId", userId);

    document.getElementById("result").innerText = "Processing...";
    console.log("Sending request to /login");

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 minute timeout
        
        const response = await fetch("/login", {
            method: "POST",
            body: formData,
            signal: controller.signal
        });

        clearTimeout(timeoutId);
        console.log("Response received:", response.status);
        const data = await response.json();
        console.log("Response data:", data);

        if (data.status === "AI") {
            alert("⚠️ AI Detected!");
            document.getElementById("result").innerText = data.message;
        }
        else if (data.status === "AUTHORIZED") {
            window.location.href = "/success";
        }
        else if (data.status === "UNAUTHORIZED") {
            alert("❌ Unauthorized user detected");
            document.getElementById("result").innerText = data.message;
        }
        else if (data.status === "ERROR") {
            alert("⚠️ " + data.message);
            document.getElementById("result").innerText = data.message;
        }
        else {
            alert("❌ Try Again");
            document.getElementById("result").innerText = "Processing failed";
        }

    } catch (error) {
        console.error("Fetch error:", error);
        let errorMsg = "Error occurred";
        
        if (error.name === 'AbortError') {
            errorMsg += ": Request timeout (taking too long)";
        } else if (error instanceof TypeError) {
            errorMsg += ": Network error or CORS issue";
        } else {
            errorMsg += ": " + error.message;
        }
        
        alert(errorMsg);
        document.getElementById("result").innerText = errorMsg;
    }
};


// No need to attach click listener here, handled via HTML onclick
