let mediaRecorder;
let audioChunks = [];
let recordedBase64 = null;

document.addEventListener("DOMContentLoaded", async () => {
    const languageSelect = document.getElementById("language");
    const generateBtn = document.getElementById("generate-btn");
    const recordBtn = document.getElementById("record-btn");
    const stopBtn = document.getElementById("stop-btn");
    const recordSection = document.getElementById("record-section");
    const textInput = document.getElementById("text");
    const statusMessage = document.getElementById("status-message");
    const audioPlayer = document.getElementById("audio-player");

    // 1. Load Languages
    const res = await fetch("/languages");
    const langs = await res.json();
    languageSelect.innerHTML = "";
    for (const [code, name] of Object.entries(langs)) {
        const opt = document.createElement("option");
        opt.value = code; opt.textContent = name;
        if (code === "hi") opt.selected = true;
        languageSelect.appendChild(opt);
    }
    languageSelect.disabled = false;

    // 2. Toggle UI & AUTO-STOP AUDIO
    document.querySelectorAll('input[name="gender"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            // KILL SWITCH: Stop sound, clear source, and hide player
            audioPlayer.pause();
            audioPlayer.src = ""; 
            audioPlayer.load(); 
            audioPlayer.classList.add("hidden");
            
            statusMessage.textContent = ""; 
            recordSection.classList.toggle('hidden', e.target.value !== 'user');
        });
    });

    // 3. Recording Logic
    recordBtn.onclick = async () => {
        // Also stop audio if user starts recording
        audioPlayer.pause();
        audioPlayer.src = "";

        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
        mediaRecorder.onstop = () => {
            const blob = new Blob(audioChunks, { type: 'audio/webm' });
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onloadend = () => {
                recordedBase64 = reader.result.split(',')[1];
                document.getElementById('record-status').textContent = "✅ Voice Captured!";
            };
        };
        mediaRecorder.start();
        recordBtn.disabled = true; stopBtn.disabled = false;
        document.getElementById('record-status').textContent = "🔴 Recording...";
    };

    stopBtn.onclick = () => {
        mediaRecorder.stop();
        recordBtn.disabled = false; stopBtn.disabled = true;
    };

    // 4. Generate Logic
    generateBtn.onclick = async () => {
        const text = textInput.value.trim();
        const gender = document.querySelector('input[name="gender"]:checked').value;

        if (!text) return alert("Please enter text.");
        if (gender === "user" && !recordedBase64) return alert("Record your voice first!");

        generateBtn.disabled = true;
        statusMessage.textContent = "Processing on GPU...";

        try {
            const response = await fetch("/generate-tts", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    text: text,
                    language: languageSelect.value,
                    gender: gender,
                    recorded_audio: recordedBase64 || ""
                })
            });
            
            const data = await response.json();
            if (response.ok) {
                audioPlayer.src = data.audio_url + "?t=" + Date.now();
                audioPlayer.classList.remove("hidden");
                audioPlayer.play();
                statusMessage.textContent = "✅ Done!";
            } else {
                statusMessage.textContent = "❌ Error: " + data.detail;
            }
        } catch (error) {
            statusMessage.textContent = "❌ Connection failed.";
        } finally {
            generateBtn.disabled = false;
        }
    };
});