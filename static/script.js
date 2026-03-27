window.uploadAudio = async function () {
    console.log("Login button clicked");

    const fileInput = document.getElementById("audioFile");
    const userId = document.getElementById("userId").value;

    if (!userId) {
        alert("Enter User ID");
        return;
    }

    if (!fileInput.files.length) {
        alert("Upload a .wav file");
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

// Attach click listener to button
console.log("Script loaded");
const loginButton = document.querySelector('button');
if (loginButton) {
    loginButton.addEventListener('click', uploadAudio);
    console.log("Button listener attached successfully");
} else {
    console.error("Button not found!");
}
